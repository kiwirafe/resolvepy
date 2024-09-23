# Resolvepy

### Resolvepy solves recurrence relations.
**Resolvepy** solves linear homogenous recurrence relations using the standard "streamline" method.


## Download
```sh
git clone https://github.com/kiwirafe/resolvepy.git
cd resolvepy
python3 setup.py install
```

## Usage
```py
from sympy import *
from resolvepy import *

n = Symbol('n')

# create the sequence
f = Recurrence('f')
f.index = n

# input the starting items
f[0] = 1
f[1] = 2

# provide a recursive formula
f[n] = f[n-1] + f[n-2]

explicit = f.resolve()

# Output the first 10 items
for i in range(10):
    value = explicit.subs(n, i).simplify()
    print("x[{}] = {}".format(i, value))
```
Note: 
1. The recursive formula must be a linear homogenous recurrence relation with constant coefficients.
2. The maximum depth of the recursive formula must be smaller than 5 (due to Abel–Ruffini theorem).
3. The amount of starting items must match the depth of the recursive formula.