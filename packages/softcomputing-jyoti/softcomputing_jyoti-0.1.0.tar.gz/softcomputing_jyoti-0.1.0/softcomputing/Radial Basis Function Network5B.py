import numpy as np
from scipy.linalg import pinv
import matplotlib.pyplot as plt

class RBF:
    def __init__(self, indim, numCenters, outdim):
        self.indim = indim
        self.outdim = outdim
        self.numCenters = numCenters
        self.centers = [np.random.uniform(-1, 1, indim) for _ in range(numCenters)]
        self.beta = 8
        self.W = np.random.random((self.numCenters, self.outdim))

    def _basisfunc(self, c, d):
        return np.exp(-self.beta * np.linalg.norm(c - d) ** 2)

    def _calcAct(self, X):
        G = np.zeros((X.shape[0], self.numCenters), float)
        for ci, c in enumerate(self.centers):
            for xi, x in enumerate(X):
                G[xi, ci] = self._basisfunc(c, x)
        return G

    def train(self, X, Y):
        rnd_idx = np.random.permutation(X.shape[0])[:self.numCenters]
        self.centers = [X[i, :] for i in rnd_idx]
        G = self._calcAct(X)
        self.W = np.dot(pinv(G), Y)

    def test(self, X):
        G = self._calcAct(X)
        Y = np.dot(G, self.W)
        return Y

if __name__ == "__main__":
    n = 100
    x = np.mgrid[-1:1:complex(0, n)].reshape(n, 1)
    y = np.sin(3 * (x + 0.5) ** 3 - 1)

    rbf = RBF(1, 10, 1)
    rbf.train(x, y)
    z = rbf.test(x)

    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'k-', label='Original')
    plt.plot(x, z, 'r-', linewidth=2, label='RBF output')
    plt.plot([c[0] for c in rbf.centers], np.zeros(rbf.numCenters), 'gs', label='Centers')
    plt.xlim(-1.2, 1.2)
    plt.legend()
    plt.show()
