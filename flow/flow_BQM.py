from dimod import BinaryQuadraticModel

bqm = BinaryQuadraticModel('BINARY')

import numpy as np

# number of pumps and pumps
n_pumps = 4
pumps = range(n_pumps)

# number of times
n_times = 2
times = range(n_times)
times_str = ['AM','PM']

# demand
demand = 20

# array with costs of pumps
costs = np.array([
    [36,27],
    [56,65],
    [48,36],
    [52,16]])

# array with flows of pumps
flows = np.array([2,7,3,8])

# array of binary variables
x = [[f'P{p}_{t}' for t in times_str] for p in pumps]
print(x)

# add variables for objective function
for p in pumps:
    for t in times:
        bqm.add_variable(x[p][t], costs[p][t])

# add first constraint for each pump: each pump must run at least once, sum over time
for p in pumps:
    # take into account variables with bias 1 (sum(x)>=1)
    c1 = [(x[p][t],1) for t in times]
    # add new linear inequality constraint function
    bqm.add_linear_inequality_constraint(
        c1, 
        lb = 1, # lower bound = 1
        ub = n_times, # upper bound = number of times
        lagrange_multiplier = 13,
        label = 'c1_pump_'+str(p)
        )

# add second constraint for each time: each pump must run at most 3 per period, sum over pump
for t in times:
    # take into account variables with bias 1 (sum(x)>=1)
    c2 = [(x[p][t],1) for p in pumps]
    # add new linear inequality constraint function (upper bound inequality)
    bqm.add_linear_inequality_constraint(
        c2, 
        constant = -3,
        lagrange_multiplier = 1,
        label = 'c2_time_'+str(t)
        )
 
# add third constraint: demand must be satisfied, equality constraint to zero
c3 = [(x[p][t],flows[p]) for t in times for p in pumps]
bqm.add_linear_equality_constraint(
    c3,
    constant = -demand, 
    lagrange_multiplier = 28 
)

# define sampler
sampler = EmbeddingComposite(DWaveSampler())