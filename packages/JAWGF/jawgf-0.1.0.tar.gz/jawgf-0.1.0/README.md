# JAWGF
Joint auto-weighted graph fusion for scalable semi-supervised learning

Python implementation of the Joint Auto-Weighted Graph Fusion method with Flexible Manifold Embedding as described in [[0]](#publications)


## Quick start

### Installation

`pip install JAWGF` 


### Implementation Example
```python
from JAWGF import joint_fusion, predict

F, Q, b = joint_fusion([X_view1, X_view2], Y, K=15)

y_soft_new = predict(new_sample, Q, b)
y_pred = y_soft_new.argmax()
```



## Citation information

Please cite [[0]](#publications) when using JAWGF in your research and reference the appropriate release version.



## Publications

[0] Bahrami, Saeedeh, Fadi Dornaika, and Alireza Bosaghzadeh. "Joint auto-weighted graph fusion and scalable semi-supervised learning." Information Fusion 66 (2021): 213-228.
