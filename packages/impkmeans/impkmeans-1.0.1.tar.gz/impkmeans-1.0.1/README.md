[![PyPI version](https://badge.fury.io/py/mcmstclustering.svg)](https://badge.fury.io/py/mcmstclustering)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

# ImpKMeans

**ImpKMeans** is an improved version of the K-Means clustering algorithm, designed to automatically determine high-quality initial centroids using:

- **Multivariate Kernel Density Estimation (KDE)**
- **KD-Tree–based radius suppression**
- **Mode-seeking peak extraction**

---

## Motivation



## 🚀 Features

- KDE-based high-density region detection  
- Intelligent centroid selection via KD-Tree radius filtering  
- Deterministic behavior with `random_state`  
- Fully compatible with scikit-learn API (`fit`, `fit_predict`, `predict`, `get_params`, `set_params`)  
- Lightweight and fast  

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install impkmeans
```

---

## Basic Usage

```bash

from sklearn.datasets import load_iris
from impkmeans import ImpKMeans
from sklearn.metrics.cluster import adjusted_rand_score

# Load dataset
data = load_iris()
X, y = data.data, data.target

model = ImpKMeans(k=7, r=0.7245, random_state=42)
labels = model.fit_predict(X)

ARI=adjusted_rand_score(y, labels)
print("Adjusted Rand Index = %0.4f"%ARI)

```

---

## Cite

If you use the code in your works, please cite the paper given below:

```bash
Şenol, A. (2024). Impkmeans: An improved version of the k-means algorithm, by determining 
optimum initial centroids, based on multivariate kernel density estimation and kd-tree. 
Acta Polytechnica Hungarica, 21(2), 111-131.
```

```bash
@article{csenol2024impkmeans,
  title={Impkmeans: An improved version of the k-means algorithm, by determining optimum initial centroids, based on multivariate kernel density estimation and kd-tree},
  author={{\c{S}}enol, Ali},
  journal={Acta Polytechnica Hungarica},
  volume={21},
  number={2},
  pages={111--131},
  year={2024}
}
```


## License

This project is licensed under the MIT License.
See the LICENSE file for details.