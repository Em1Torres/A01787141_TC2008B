import numpy as np
import matplotlib.pyplot as plt

matrix = np.zeros((8, 8))
S = np.zeros((matrix.size, matrix.size))

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                try:
                    S[np.ravel_multi_index((i, j), matrix.shape), np.ravel_multi_index((i + x, j + y), matrix.shape)] = 1
                except:
                    continue

print(matrix)
print(np.where(S[9,:] != 0))
plt.imshow(S)
plt.show()

d_base = 0.3
D = np.zeros((matrix.size, matrix.size))

for n in range(matrix.size):
    for m in range(matrix.size):
        if n == m:
            continue
        i, j = np.unravel_index(n, matrix.shape)
        x, y = np.unravel_index(m, matrix.shape)
        D[n, m] = d_base * np.linalg.norm(np.asarray([i - x, j - y]))

plt.matshow(D)
plt.show()

P = S.copy()
for i in range(P.shape[0]):
    P[i] = P[i] / np.sum(P[i])

print(P)
plt.imshow(P)
plt.show()

path = [0,1,2,3,4,5,17,18,19]
p = 1
p_= []

valid_path = True
for i in range(len(path)-1):
    if S[path[i],path[i + 1]] == 1:
        print(f"Step from {path[i]} to {path[i + 1]} is valid.")
        p_.append(P[path[i],path[i+1]])
    else:
        print(f"Step from {path[i]} to {path[i + 1]} is invalid.")
        valid_path = False
        break

p_=np.asarray(p_)
p_ = -np.log(p_.prod())


print(f"Path: {valid_path}")
print(f"Cost path: {p_}")

