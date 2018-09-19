a = '../input/actual.txt'

infileFlag = True

import time
from collections import deque

a = [1]*100000

start = time.time()
a.pop(0)
print time.time() - start

start = time.time()
b=deque(a)
b.pop()
print time.time() - start
