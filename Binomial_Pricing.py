import numpy as np
import scipy.stats as ss
import time

def BinomialTreeVer1(type, S0, K, r, sigma, T, N=2000):
    # time frame
    deltaT = T / N

    # movement factor
    u = np.exp(sigma * np.sqrt(deltaT))
    d = 1 / u

    # first version we want to do this in a matrix
    # this could be really slow
    fs = [[ 0.0 for j in range(i + 1)] for i in range(N + 1)]

    disc = np.exp(r * deltaT)
    p = (a - d) / (u - d)

    for j in range(i+1):
        if type == 'c':
            fs[N][j] = max(S0*u**j*d**(N-j)-k,0.0)
        else:
            fs[N][j] = max(-S0*u**j*d**(N-j)+k,0.0)

    for i in range(N-1, -1, -1):
        for j in range(i + 1):
            fs[i][j] = np.exp(-r * deltaT) * (p * fs[i + 1][j + 1] + (1-p) * fs[i + 1][j])


    return fs[0][0]

