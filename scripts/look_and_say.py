#!/usr/bin/env python

import sys
import time
from profiling import profile_decorator

from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

from intpy import deterministic, initialize_intpy

@deterministic
def look_and_say_sequence(n):
    starting_sequence="1223334444"
    i = 0
    while i < n:
        if i == 0:
            current_sequence = starting_sequence
        else:
            count = 1
            temp_sequence = ""
            for j in range(1, len(current_sequence)):
                if current_sequence[j] == current_sequence[j-1]:
                    count += 1
                else:
                    temp_sequence = temp_sequence + str(count) \
                                    + current_sequence[j-1]
                    count = 1
            temp_sequence = temp_sequence + str(count)\
                + current_sequence[len(current_sequence) - 1]

            current_sequence = temp_sequence
        i += 1
    return current_sequence


if len(sys.argv) < 2:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' N')
    print('Please specify a number.')
    sys.exit()
@profile_decorator
@initialize_intpy(__file__)
def main():
    N = int(sys.argv[1])    
    look_and_say_sequence(N)
    
    


if __name__ == '__main__':
    main()
