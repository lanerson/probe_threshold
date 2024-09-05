
import numpy as np
import sys
from profiling import profile_decorator
import time

from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

from intpy import initialize_intpy, deterministic

@deterministic
def belief_propagation(N):    
    dim = 5000
    A = np.random.rand(dim, dim)
    x = np.ones((dim,))

    for i in range(N):
        x = np.log(np.dot(A, np.exp(x)))
        x -= np.log(np.sum(np.exp(x)))    
    
    return x

@profile_decorator
@initialize_intpy(__file__)
def main(N):
    y = belief_propagation(N)
    

if __name__ == '__main__':
    N = int(sys.argv[1])
    main(N)
    
