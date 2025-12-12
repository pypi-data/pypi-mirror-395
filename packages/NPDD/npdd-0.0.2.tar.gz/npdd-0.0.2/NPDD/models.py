import pickle
import torch
import os

from torch.utils.data import Dataset
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from tqdm import tqdm
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATv2Conv, global_mean_pool
from torch_geometric.nn.models import AttentiveFP
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, r2_score, mean_squared_error, mean_absolute_error
from scipy.stats import spearmanr


hidden_dim = 128
NUM_POCKETS = 30
NUM_TOP_POCKETS = 15
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def normalize_binding(x, xmin=0, xmax=6):
    x = np.log10(x)
    x = np.clip(x, xmin, xmax)
    return (x - xmin) / (xmax - xmin)

class LigandPocketDataset(Dataset):
    def __init__(self, DATA):
        self.DATA = DATA

    def __len__(self):
        return len(self.DATA)

    def __getitem__(self, idx):
        return self.DATA[idx]

class PocketAttention(nn.Module):
    def __init__(self, embed_dim, num_heads=4):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
    
    def forward(self, pocket_embs, mask=None):
        """
        pocket_embs: [batch_size, max_length, embed_dim]
        mask: optional boolean mask of shape [batch_size, max_length] where True indicates padding
        """
        batch_size, max_length, _ = pocket_embs.size()
        
        if mask is None:
            attn_mask = torch.triu(torch.ones(max_length, max_length, device=pocket_embs.device), diagonal=1).bool()
        else:
            attn_mask = None
        key_padding_mask = mask if mask is not None else None

        attended, _ = self.attn(pocket_embs, pocket_embs, pocket_embs,
                                attn_mask=attn_mask, key_padding_mask=key_padding_mask)
        return attended  # [batch_size, max_length, embed_dim]


class LigandPocketBindingPredictor(nn.Module):
    def __init__(
        self,
        ligand_node_feat_dim=1,
        edge_dim=1,
        farm_dim=768,
        pocket_esm_dim=2560,
        protein_esm_dim=1280,
        hidden_dim=256
    ):
        super().__init__()

        # --- Replace AttentiveFP with a GATv2-based ligand encoder ---
        num_heads = 4
        gat_hidden = hidden_dim // num_heads

        self.ligand_gnn = nn.ModuleList([
            GATv2Conv(
                in_channels=ligand_node_feat_dim if i == 0 else hidden_dim,
                out_channels=gat_hidden,
                heads=num_heads,
                edge_dim=edge_dim,
                dropout=0.1
            ) for i in range(3)
        ])
        self.ligand_norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(3)])

        # --- FARM projection ---
        self.farm_proj = nn.Sequential(
            nn.Linear(farm_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim)
        )

        # --- Pocket ESM projection ---
        self.pocket_esm_proj = nn.Sequential(
            nn.Linear(pocket_esm_dim, hidden_dim * 4),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim * 4),
            nn.Linear(hidden_dim * 4, hidden_dim * 2),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim * 2)
        )

        # --- Pocket attention (unchanged) ---
        self.pocket_attn = PocketAttention(embed_dim=hidden_dim * 2, num_heads=4)

        # --- Fusion and output ---
        self.fusion_proj = nn.Sequential(
            nn.Linear(4 * hidden_dim, 2 * hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(2 * hidden_dim),
            nn.Linear(2 * hidden_dim, 1)
        )

    def encode_ligand(self, x, edge_index, edge_attr, batch):
        for conv, norm in zip(self.ligand_gnn, self.ligand_norms):
            x = conv(x, edge_index, edge_attr)
            x = F.relu(x)
            x = norm(x)
        graph_emb = global_mean_pool(x, batch)
        return graph_emb

    def forward(self, data):
        x, edge_index, edge_attr, farm, esm_embedding, pocket_emb, batch = (
            data.x, data.edge_index, data.edge_attr,
            data.farm, data.esm_embedding, data.pocket_emb, data.batch
        )

        # Ligand encoding (via GATv2)
        ligand_graph_emb = self.encode_ligand(x, edge_index, edge_attr, batch)

        # FARM projection
        farm_emb = self.farm_proj(farm)
        ligand_emb = torch.cat([ligand_graph_emb, farm_emb], dim=-1)

        # Pocket embedding projection
        proj_pocket_embs = torch.stack([self.pocket_esm_proj(p) for p in pocket_emb])

        # Pocket attention
        attended_pocket_embs = self.pocket_attn(proj_pocket_embs)

        # Fusion
        ligand_expanded = ligand_emb.unsqueeze(1).expand(-1, proj_pocket_embs.size(1), -1)
        fusion = torch.cat([attended_pocket_embs, ligand_expanded], dim=-1)

        # Output
        logits = self.fusion_proj(fusion).squeeze(-1)
        all_props = torch.sigmoid(logits)
        return all_props

class DMNLoss(nn.Module):
    def __init__(self, eps=1e-6):
        super().__init__()
        self.eps = eps

    def forward(self, pi, mu, sigma, target):
        target = target.unsqueeze(1)  # (batch, 1)
        prefac = 1.0 / (sigma * np.sqrt(2 * np.pi))
        exponent = -0.5 * ((target - mu) / sigma) ** 2
        prob = pi * prefac * torch.exp(exponent)
        prob = prob.sum(dim=1)
        nll = -torch.log(prob + self.eps)
        return nll.mean()

# ================== Losses ======================
def bag_level_loss_1(props, label):
    props = props.float()
    label = label.float()
    bag_prob = torch.mean(props, dim=1)
    loss = F.mse_loss(bag_prob, label)
    return loss

def bag_level_loss_2(props, label):
    props = props.float()
    label = label.float()
    weights = props / torch.sum(props, dim=1, keepdim=True)  # normalize along dim=1
    bag_pred = torch.sum(weights * props, dim=1)
    loss = F.mse_loss(bag_pred, label)
    return loss

def bag_level_loss_3(props, label, power=2.0, eps=1e-5):
    """
    props: [batch_size, num_instances] - instance-level predictions
    label: [batch_size] - bag-level labels
    power: controls sharpness of weighting (>1 makes the mean sharper)
    """
    props = props.float()
    label = label.float()
    weights = (props ** power) / (torch.sum(props ** power, dim=1, keepdim=True) + eps)
    bag_pred = torch.sum(weights * props, dim=1)
    loss = F.mse_loss(bag_pred, label)
    return loss
    
def Pooling_1(props):
    return torch.mean(props, dim=1)

def Pooling_2(props, eps=1e-3):
    """
    props: [batch_size, num_instances] - predicted probabilities per instance
    returns: [batch_size] - bag probabilities (weighted mean)
    """
    props = props.float()
    weights = props / (torch.sum(props, dim=1, keepdim=True) + eps)
    bag_pred = torch.sum(weights * props, dim=1)
    return bag_pred

def Pooling_3(props, power=2.0, eps=1e-8):
    """
    props: [batch_size, num_instances] - instance-level predictions
    power: controls sharpness of weighting (>1 makes the mean sharper)
    returns: [batch_size] - bag-level predictions (weighted mean)
    """
    props = props.float()
    
    # Compute normalized sharp weights
    weights = (props ** power) / (torch.sum(props ** power, dim=1, keepdim=True) + eps)
    
    # Weighted mean pooling
    bag_pred = torch.sum(weights * props, dim=1)
    
    return bag_pred
