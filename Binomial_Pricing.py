import numpy as np
import scipy.stats as ss
import time

def BinomialTree(type, S0, K, r, sigma, T, N, extype, divi=[[],[]]):
    def expiCall(und, strike):
        return np.maximum(und - strike, 0)
    def expiPut(und, strike):
        return np.maximum(strike - und, 0)
    def earlyCall(ExpOpt, und, strike):
        return np.maximum(und - strike, ExpOpt)
    def earlyPut(ExpOpt, und, strike):
        return np.maximum(ExpOpt, strike - und)
    def earlyEuro(ExpOpt, und, strike):
        return np.maximum(ExpOpt, 0)

    if type == 'c':
        expi = expiCall
        early = earlyCall
    else:
        expi = expiPut
        early = earlyPut
    if extype == "er":
        early = earlyEuro

    deltaT = T / N
    u = np.exp(sigma * np.sqrt(deltaT))
    d = 1 / u

    a = np.exp(r * deltaT)
    p = (a - d) / (u - d)

    dividends = [[],[]]
    if (np.size(divi) > 0 and divi[0][0] < T):
        lastdiv = np.nonzero(np.array(divi[0][:]) <= T)[0][-1]
        dividends[0] = divi[0][:lastdiv + 1]        
        dividends[1] = divi[1][:lastdiv + 1] 
    if np.size(dividends) > 0:
        dividendsStep = np.floor(np.multiply(dividends[0],1 / deltaT))
    else:
        dividendsStep = []  
    if np.size(dividends) > 0:
        pvdividends = np.sum(np.multiply(dividends[1],np.exp(np.multiply(dividendsStep,-r * deltaT))))
    else:
        pvdividends = 0
    S0 = S0 - pvdividends
    currentDividend = 0
    
    und = np.array([S0 * u ** (N - j) * d ** j for j in range(N + 1)])
    strike = np.array([K for i in range(N + 1)])

    ExpOpt_step_leaves = expi(und, strike)

    # logic is here:
    # we first deduct pv of dividend to S0 for all price
    # this is no problem for eurpean option because we only
    # care about expiration date, and the discount will yield same result
    # for american options, for each step that has dividend, whenever we check
    # early
    # excercise, we want to add back the dividend for price.
    # at expi, the price is same anyway because all dividend effect is included
    # as we roll back, we want to add back dividend whenever there's one to S


    for i in range(N):
        # roll back N times
        ExpOpt_step_leaves[:-1] = np.exp(-r * deltaT) * \
            (p * ExpOpt_step_leaves[:-1] + (1 - p) * ExpOpt_step_leaves[1:])
        und = und / u

        currentDividend = currentDividend / a
        # discount dividend
        if (i in dividendsStep):
            div = dividends[1][np.nonzero(dividendsStep == (i))[0]]            
            currentDividend = currentDividend + div
        ExpOpt_step_leaves = early(ExpOpt_step_leaves, und + currentDividend, strike)

    return ExpOpt_step_leaves[0]








if __name__ == "__main__":
    t = time.time()
    div = [[0.9,1.9,2.9],[0,0,0]]
    print(BinomialTree('c', 100, 100, 0.05, 0.3, 3, 1500, "er", div))
    # one should only excercise american call for dividends.
    # or excercise american put for interest.
    # since no dividends were added here yet, call should be the same
    # put should be higher for american
    div = [[0.9,1.9,2.9],[10,10,10]]
    print(BinomialTree('c', 100, 100, 0.05, 0.3, 3, 1500, "er", div))
    elapsed = time.time() - t
    print(elapsed)