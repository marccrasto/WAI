import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
a = [2.6666e+04, 7.1680e+03, 0.0000e+00, -1.8229e+04, 3.2000e+01, -1.1093e+04, 2.2700e+00, 2.4300e+00, 2.4000e+00]
b = scaler.inverse_transform(a)
print(a)
print(b)
