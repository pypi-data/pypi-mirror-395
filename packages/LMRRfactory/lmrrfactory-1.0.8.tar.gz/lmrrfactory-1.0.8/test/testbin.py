import numpy as np

Trange = np.linspace(300,2000,35)
print(Trange)
indices = [np.where(Trange == 300)[0][0],np.where(Trange == 1000)[0][0],np.where(Trange == 2000)[0][0]]
print(indices)