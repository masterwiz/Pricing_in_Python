import BSM as bsm
import numpy as np
import time 
import scipy.interpolate as si

def FiniteDiff(option, params):
    NAS = params.NAS
    [S0, K, sigma, T, r, divi, american] = [option.S0, \
        option.K, option.sigma, option.T, \
        option.r, option.divi, option.american]
    


    delta = np.array([0 for i in range(NAS)])
    gamma = np.array([0 for i in range(NAS)])
    theta = np.array([0 for i in range(NAS)])

    ds = 2 * K / NAS
    # von Neumann Stability
    dt = 0.9 / (sigma ** 2 * NAS ** 2) # for stability of single asset vanilla option
    NTS = int(T / dt) + 1
    dt = T / NTS

    VC = np.array([ 0 for i in range(NAS + 1)])
    VP = np.array([ 0 for i in range(NAS + 1)])
    Kk = np.array([ K for i in range(NAS + 1)])
    S = np.array([i * ds for i in range(NAS + 1)])

    VC = np.maximum(S - Kk, 0)
    VP = np.maximum(- S + Kk, 0)

    for k in range(1, int(NTS)):
        # delta is respect to the change of  stock price
        delta = (VC[2:] - VC[:-2]) / (2 * ds)
        # so is gamma, 
        gamma = (VC[2:] + VC[:-2] - 2 * VC[1:-1]) / (ds * ds)
        # all above is at middle i [1:-1]
        # so is the way we esitmate theta

        # we got theta using the formular
        theta = -0.5 * (sigma ** 2) * np.power(S[1:-1],2) * gamma - r * (S[1:-1]) * delta + r * VC[1:-1]
        
        # all above is at time i, now we roll back to time i-1
        # because time decay
        VC[1:-1] = VC[1:-1] - dt * theta
        
        # we also calculate edge condition when S = 0 or S = NAS largest
        VC[0] = VC[0] * (1 - r * dt)
        VC[NAS] = 2 * VC[NAS - 1] - VC[NAS - 2]

        # similar process for put
        delta = (VP[2:] - VP[:-2]) / (2 * ds)
        gamma = (VP[2:] + VP[:-2] - 2 * VP[1:-1]) / (ds * ds)
        theta = -0.5 * (sigma ** 2) * np.power(S[1:-1],2) * gamma - r * (S[1:-1]) * delta + r * VP[1:-1]

        VP[1:-1] = VP[1:-1] - dt * theta
        
        VP[0] = VP[0] * (1 - r * dt)
        VP[NAS] = 2 * VP[NAS - 1] - VP[NAS - 2]

    tck=si.splrep(S,VC[:])
    option.call.price=si.splev(S0,tck,der=0)   
    tck=si.splrep(S,VP[:])
    option.put.price=si.splev(S0,tck,der=0)   


if __name__ == "__main__":
    S0 = 100.0
    K = 100.0
    r=0.1
    sigma = 0.30
    T = 3
    
    class param():
        def __init__(self):
            self.NAS = 300
    p = param()

    oc=bsm.optionClass(S0, K, r, sigma, T, False)

    t=time.time()

    #FiniteDiff(oc, p)
    bsm.BlackScholesInfo(oc)

    elapsed = time.time()-t
    print(elapsed)
    print(oc.call.price)
    print(oc.put.price)




