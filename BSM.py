import numpy as np 
import scipy.stats as ss
import time

def d1(S0, K, r, sigma, T):
    return (np.log(S0 / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))

def d2(S0, K, r, sigma, T):
    return (np.log(S0 / K) + (r - sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))

def BlackScholes(cp, S0, K, r, sigma, T):
    if cp == "c":
        return S0 * ss.norm.cdf(d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S0, K, r, sigma, T))
    else:
        return -S0 * ss.norm.cdf(-d1(S0, K, r, sigma, T)) + K * np.exp(-r * T) * ss.norm.cdf(-d2(S0, K, r, sigma, T))

class optionGreek:
    price = 0
    delta = 0
    gamma = 0
    theta = 0

class optionClass:
    [S0, K, r, sigma, T] = [0,0,0,0,0]
    divi = [[],[]]
    american = 'false'
    call = optionGreek()
    put = optionGreek()

    def __init__(self, S0, K, r, sigma, T, american):
        self.S0 = S0
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T
        self.american = american

def BlackScholesInfo(option):
    S0, K, r, sigma, T = option.S0, option.K, option.r, option.sigma, option.T
    td1 = d1(S0, K, r, sigma, T)
    td2 = d2(S0, K, r, sigma, T)

    option.call.price = BlackScholes('c',S0, K, r, sigma, T)
    option.put.price = BlackScholes('p',S0, K, r, sigma, T)

    option.call.delta = ss.norm.cdf(td1)
    option.put.delta = ss.norm.cdf(td1) - 1

    NPrime = ((2*np.pi)**(-1/2))*np.exp(-0.5*(td1)**2)
    option.call.gamma = NPrime/(S0*sigma*T**(1/2))
    option.put.gamma = option.call.gamma

    option.call.theta=(NPrime)*(-S0*sigma*0.5/np.sqrt(T))-r*K * np.exp(-r * T) * ss.norm.cdf(td2)
    option.put.theta=(NPrime)*(-S0*sigma*0.5/np.sqrt(T))+r*K * np.exp(-r * T) * ss.norm.cdf(-td2)


def main():
    S0 = 100.0
    K = 100.0
    r=0.1
    sigma = 0.30
    T = 3

    oc=optionClass(S0, K, r, sigma, T, False)
    t=time.time()
    for i in range(1000):
        BlackScholesInfo(oc)
    elapsed = time.time()-t
    print(oc.put.price)
    print(elapsed)


if __name__ == "__main__":
    main()
