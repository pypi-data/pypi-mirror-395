import torch
from importlib import resources
from .models import LigandPocketBindingPredictor, Pooling_3, bag_level_loss_1, bag_level_loss_2, bag_level_loss_3, device, NUM_POCKETS, NUM_TOP_POCKETS, spearmanr, r2_score
from tqdm import tqdm
import pickle
from tqdm import tqdm
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from scipy.stats import spearmanr


def Predict(test_loader, verbose=True, train_mode=False):
    if not train_mode:
        model = LigandPocketBindingPredictor()
        weight_path = resources.files('NPDD.weights').joinpath('NPASS_pocket_mse_gat_best_1.pt')
        model.load_state_dict(torch.load(weight_path, map_location=device))
    model = model.to(device)
    model.eval()
    results = []

    with torch.no_grad():
        for data in tqdm(test_loader):
            data = data.to(device)
            all_props = model(data)  # [batch_size, num_instances]
            if all_props.size(1) > NUM_TOP_POCKETS:
                testues, _ = torch.topk(all_props, NUM_TOP_POCKETS, dim=1)
            else:
                testues, _ = all_props, None
            pooled = Pooling_3(testues).detach().cpu()  # [batch_size]
            label = data.normed_label  # [batch_size]
            results.append([label.cpu(), pooled])
            loss = bag_level_loss_2(testues, label).mean()

        # Concatenate all labels and predictions for metrics
        gt = torch.cat([i[0] for i in results]).cpu().numpy()
        pr = torch.cat([i[1] for i in results]).cpu().numpy()

    spearman = spearmanr(gt, pr).correlation
    r2 = r2_score(gt, pr)
    if verbose:
        print(f'Spearman: {spearman:.4f}')
        print(f'R2      : {r2:.4f}')

    return {'Groundtruth': gt, 'Prediction': pr}


def Training(dataset, epochs=10, lr=1e-4, device=device):

    train_loader = dataset['train_loader']
    val_loader = dataset['val_loader']
    test_loader = dataset['test_loader']

    model = LigandPocketBindingPredictor()
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    best_metric = 0
    best_epoch = 0

    for epoch in range(1, epochs):
        model.train()
        train_loss = 0
        for data in tqdm(train_loader, desc=f'epoch {epoch}/{epochs}, best spearman = {best_metric:.2f}'):
            data = data.to(device)
            all_props = model(data).to(device)
            if all_props.size(1) > NUM_TOP_POCKETS:
                values, _ = torch.topk(all_props, NUM_TOP_POCKETS, dim=1)
            else:
                values = all_props
            label = data.normed_label
            if epoch <= 5:
                loss = bag_level_loss_1(values, label).mean()
            elif epoch <= 10:
                loss = bag_level_loss_2(values, label).mean()
            else:
                loss = bag_level_loss_3(values, label).mean()
            train_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # ========== Validation ==========
        infer = Predict(val_loader, verbose=False, train_mode=True)
        gt, pr = infer['Groundtruth'], infer['Prediction']

        current_loss = train_loss / len(train_loader)

        spearman = spearmanr(gt, pr).correlation
        r2 = r2_score(gt, pr)
        if spearman > best_metric:
            best_metric = spearman
            best_epoch = epoch
            best_model = model.state_dict()
        last_model = model.state_dict()
        print(f'Training loss: {current_loss:.4f}, best val spearman: {best_metric:.4f}, val spearman: {spearman:.4f}, val r2: {r2:.4f}')

    print('---------TEST---------')
    model.load_state_dict(best_model, map_location=device)
    Predict(test_loader, train_mode=True)
    return best_model, last_model
