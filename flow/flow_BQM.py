from dimod import BinaryQuadraticModel

bqm = BinaryQuadraticModel('BINARY')

import numpy as np

# number of pumps
pumps = 4

# number of periods
time = 2

# array with costs of pumps
costs = np.array([[36,27],[56,65],[48,36],[52,16]])

# array with flows of pumps
flows = np.array([[2,2],[7,7],[3,3],[8,8]])

# add variables
for p in pumps:
    for t in time:
        bqm.add_variable(x[p][t])