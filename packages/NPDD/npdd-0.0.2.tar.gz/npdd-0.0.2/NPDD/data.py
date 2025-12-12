
from importlib import resources
import torch
from torch_geometric.loader import DataLoader
import pickle
from models import LigandPocketDataset, normalize_binding, device, NUM_POCKETS, NUM_TOP_POCKETS


def load_dataset(data, batch_size=32, verbose=True, example=True):

    if example:
        with resources.files("NPDD.data_files").joinpath(f'ki_training_w_pocket.pkl').open("rb") as f:
            data = pickle.load(f)

    train = data['train']
    val = data['val']
    test = data['test']

    if verbose:
        print('Training data: ')
        print('\t#Positive samples: ', len([i.binary_label for _,i in train.items() if i.binary_label==1]))
        print('\t#Negative samples: ', len([i.binary_label for _,i in train.items() if i.binary_label==0]))

        print('Validation data: ')
        print('\t#Positive samples: ', len([i.binary_label for _,i in val.items() if i.binary_label==1]))
        print('\t#Negative samples: ', len([i.binary_label for _,i in val.items() if i.binary_label==0]))

        print('Test data: ')
        print('\t#Positive samples: ', len([i.binary_label for _,i in test.items() if i.binary_label==1]))
        print('\t#Negative samples: ', len([i.binary_label for _,i in test.items() if i.binary_label==0]))

    for s in [train, val, test]:
        for k, v in s.items():
            v.farm = v.farm.sum(0).unsqueeze(0) # (1,768)
            v.normed_label = normalize_binding(v.raw_label)
            pocket_esm_list = v.pocket_emb
            num_pockets = min(len(pocket_esm_list), NUM_POCKETS)
            pocket_esm_list = torch.stack([pocket_esm_list[i] for i in range(num_pockets)]).unsqueeze(0)
            try:
                batch_size, current_pockets, feat_dim = pocket_esm_list.size()
            except:
                pocket_esm_list = pocket_esm_list.squeeze().unsqueeze(0)
                batch_size, current_pockets, feat_dim = pocket_esm_list.size()

            padding = torch.zeros(batch_size, NUM_POCKETS - current_pockets, feat_dim, device=pocket_esm_list.device)
            pocket_esm_list = torch.cat([pocket_esm_list, padding], dim=1)
            v.pocket_emb = pocket_esm_list

    train = {k: v for k, v in train.items()}
    val = {k: v for k, v in val.items()}
    test = {k: v for k, v in test.items()}

    del data

    train = list(train.values())
    val = list(val.values())
    test = list(test.values())
    train_dataset = LigandPocketDataset(train)
    val_dataset = LigandPocketDataset(val)
    test_dataset = LigandPocketDataset(test)
    del train; del val; del test

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    del train_dataset; del val_dataset; del test_dataset

    return {'train_loader': train_loader, 'val_loader': val_loader, 'test_loader': test_loader}