class Neuron:
    def __init__(self, weights):
        self.weightv = weights
        self.activation = 0

    def act(self, m, x):
        a = 0
        for i in range(m):
            a += x[i] * self.weightv[i]
        return a

class Network:
    def __init__(self, a, b, c, d):
        self.nrn = [Neuron(a), Neuron(b), Neuron(c), Neuron(d)]
        self.output = [0] * 4

    def threshld(self, k):
        return 1 if k >= 0 else 0

    def activation(self, patrn):
        for i in range(4):
            self.nrn[i].activation = self.nrn[i].act(4, patrn)
            self.output[i] = self.threshld(self.nrn[i].activation)
            print(f"Neuron {i} activation: {self.nrn[i].activation}, output: {self.output[i]}")

def main():
    patrn1 = [1, 0, 1, 0]
    patrn2 = [0, 1, 0, 1]
    wt1 = [0, -3, 3, -3]
    wt2 = [-3, 0, -3, 3]
    wt3 = [3, -3, 0, -3]
    wt4 = [-3, 3, -3, 0]

    print("\nHOPFIELD NETWORK WITH 4 NEURONS")
    H1 = Network(wt1, wt2, wt3, wt4)

    print("\nTesting pattern 1010")
    H1.activation(patrn1)

    print("\nTesting pattern 0101")
    H1.activation(patrn2)

if __name__ == "__main__":
    main()
