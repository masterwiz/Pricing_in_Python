import numpy as np
import scipy.stats as ss
import time

def BinomialTree(type, S0, K, r, sigma, T, N=10):
    # time frame
    deltaT = T / N

    # movement factor
    u = np.exp(sigma * np.sqrt(deltaT))
    d = 1 / u

    fs = np.array([np.maximum(S0 * u ** (N - i) * d ** i - K, 0) for i in range(N + 1)])

    disc = np.exp(r * deltaT)
    p = (disc - d) / (u - d)
    
    #step = N + 1
    #while True:
    #    step -= 1
    #    for i in range(step):
    #        # this is where time spent because iteration and two while loop
    #        # if we can make this a matrix operation
    #        fs[i] = np.exp(-r * deltaT) * (p * fs[i] + (1 - p) * fs[i + 1])
    #    if i == 0:
    #        break
    #    if i%100==0:
    #        print("processing")
    
    # much faster without iteration, using matrix
    for i in range(N): # we simply rollback n steps
        fs[:-1] = np.exp(-r*deltaT)*(p*fs[:-1]+(1-p)*fs[1:])

           
    return fs[0]




if __name__ == "__main__":
    t = time.time()
    print(BinomialTree('c', 100, 100, 0.1, 0.3, 3, 5000))
    elapsed = time.time() - t
    print(elapsed)