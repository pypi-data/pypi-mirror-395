# NPDD

**Natural Product - Protein Binding Affinity Prediction Toolkit**

---

## Installation

### Create environment:
```bash
conda create --name npdd
conda activate npdd
```
### Install package
```bash
pip install NPDD
```

### Prepare Data

Prepare your dataset or load a prepared NPASS dataset.

```python
from NPDD import *
dataset = load_dataset(example=True)
```
IC50, Ki, Kd and full NPASS datasets are at https://huggingface.co/datasets/kaiya21/NPDD

### Training
```python
best_model, last_model = Training(dataset)
```

### Inference
```python
test_loader = dataset['test_loader']
results = Predict(test_loader)
```