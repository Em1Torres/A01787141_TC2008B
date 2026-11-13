import numpy as np
import matplotlib.pyplot as plt
m=8
n=8
A = np.zeros((m, n), dtype=int)
S = np.zeros((A.size, A.size), dtype=int)
D = np.zeros((A.size, A.size), dtype=int)

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                if 0 <= i + x < A.shape[0] and 0 <= j + y < A.shape[1]:
                    S[np.ravel_multi_index((i, j), A.shape), np.ravel_multi_index((i + x, j + y), A.shape)] = 1

D[:] = A.size
D[S != 0] = 1
np.fill_diagonal(D, 0)
for k in range(A.size):
    D = np.minimum(D, D[:, k, np.newaxis] + D[np.newaxis, k, :])

print (np.where(S[9,:] != 0))
# plt.imshow(S, cmap='gray')
# plt.show()
plt.imshow(D, cmap='gray')
plt.show()
