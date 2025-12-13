# ANDClust

ANDClust is a clustering algorithm based on **Adaptive Neighborhood Density** and **MST expansion with local density ratios**.  
This package implements the final optimized version of the ANDClust algorithm.

## Installation

```bash
pip install andclust
```

## Usage

```bash
from andclust import ANDClust
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score

data=load_iris()
X,y=data['data'],data['target']

scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)

model = ANDClust(N=2,k=14,eps=0.113) # If you want to change kernel and band_with use model = ANDClust(N=2,k=14,eps=0.113,kernel='gaussian',b_width=0.025) default values for optional parameter krnl='gaussian', b_width=0.5 options for kernel are{“gaussian”, “tophat”, “epanechnikov”,
“exponential”, “linear”, “cosine”}
labels = model.fit_predict(X)

ARI=adjusted_rand_score(labels,y)
print("ARI=", ARI)
model.plotGraph("ARI",ARI,dataset_name)
```

Features

Adaptive neighborhood density (AND)

Kernel Density Estimation–based cluster core detection

MST expansion using local ratio constraints

Noise handling

High performance (KDTree + vectorized operations)


##Citation

If you use this algorithm in research, please cite the corresponding paper.

```text
Şenol, A. (2024). ANDClust: An Adaptive Neighborhood Distance-Based Clustering Algorithm to Cluster Varying Density and/or Neck-Typed Datasets. Advanced Theory and Simulations, 7(4), 2301113.
```

#BibTeX

```text
@article{csenol2024andclust,
  title={ANDClust: An Adaptive Neighborhood Distance-Based Clustering Algorithm to Cluster Varying Density and/or Neck-Typed Datasets},
  author={{\c{S}}enol, Ali},
  journal={Advanced Theory and Simulations},
  volume={7},
  number={4},
  pages={2301113},
  year={2024},
  publisher={Wiley Online Library}
}
```
---

## LICENSE **

```text
MIT License

Copyright (c) 2025 Ali Şenol

Permission is hereby granted, free of charge, to any person obtaining a copy
...