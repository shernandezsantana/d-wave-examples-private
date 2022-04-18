# import model
from dimod import ConstrainedQuadraticModel, quicksum, Binary
from dwave.system import LeapHybridCQMSampler
import numpy as np
import random
import itertools

# problem set up
num_packages = 300

# priority of each package, 3 = high priority, 1 = low priority
priority = [random.choice([1,2,3])  for i in range(num_packages)]

# number of days since each package was ordered
days_since_order = [random.choice([0,1,2,3])  for i in range(num_packages)]

# weight of each package
cost = [random.randint(1,100)  for i in range(num_packages)]

# maximum weight and number of packages the truck can handle
max_weight = 3000
max_parcels = 100

# weights for the objective function
obj_weight_priority = 1.0
obj_weight_days = 1

num_items = len(cost)

# build the CQM
cqm = ConstrainedQuadraticModel()

# create the binary variables
bin_variables = [Binary(i) for i in range(num_items)]

# - - - - - - - - - - Objective functions - - - - - - - - - -
# build an objective to consider priority shipping
objective1 = - obj_weight_priority * quicksum(priority[i] * bin_variables[i] for i in range(num_items))

# build an objective to consider number of days since the order was placed
objective2 = - obj_weight_days * quicksum(days_since_order[i] * bin_variables[i] for i in range(num_items))

# add the objectives to the CQM
cqm.set_objective(objective1 + objective2)

# - - - - - - - - - - Constraints - - - - - - - - - -
# add the maximum capacity constraint
cqm.add_constraint(quicksum(cost[i] * bin_variables[i] for i in range(num_items)) <= max_weight, label='max_capacity')

# add the maximum parcel (or truck size) constraint
cqm.add_constraint(quicksum(bin_variables[i] for i in range(num_items)) == max_parcels, label='max_parcels')

# - - - - - - - - - - Submit to the CQM sampler - - - - - - - - - -
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, time_limit=10)
print(sampleset.info)

# - - - - - - - - - - Process the results - - - - - - - - - -
feasible_sols = np.where(sampleset.record.is_feasible == True)
print(feasible_sols)

if len(feasible_sols[0]):
    first_feasible_sol = np.where(sampleset.record[feasible_sols[0][0]][0] == 1)

    # characterize the problem
    problem_array = np.zeros((3,4)).astype(int)
    for i in range(num_items):
        problem_array[-1 * (priority[i]-3)][-1 * (days_since_order[i]-3)] += 1

    print("\n********** PROBLEM ********** ")
    print('            Days since order was placed')
    print('{:>5s}{:>5s}{:^5s}{:^5s}{:^5s}'.format('Priority |','3','2','1','0'))
    print('-' * 40)

    for i in range(3):
        print('{:>5s}{:>10s}{:^5s}{:^5s}{:^5s}'.format(str(-1*(i-3)),str(problem_array[i][0]),str(problem_array[i][1]),
        str(problem_array[i][2]),str(problem_array[i][3])))

    # characterize the solution
    solution_array = np.zeros((3,4)).astype(int)
    total_weight = 0
    total_items = len(first_feasible_sol[0])
    for i in range(num_items):
        if i in first_feasible_sol[0]:
            solution_array[-1 * (priority[i]-3)][-1 * (days_since_order[i]-3)] += 1
            total_weight += cost[i]

    print("\n********** SOLUTION ********** ")
    print('            Days since order was placed')
    print('{:>5s}{:>5s}{:^5s}{:^5s}{:^5s}'.format('Priority |','3','2','1','0'))
    print('-' * 40)

    for i in range(3):
        print('{:>5s}{:>10s}{:^5s}{:^5s}{:^5s}'.format(str(-1*(i-3)),str(solution_array[i][0]),str(solution_array[i][1]),
        str(solution_array[i][2]),str(solution_array[i][3])))

    print("\nTotal number of selected items:",total_items)
    print("Total weight of selected items:",total_weight)
    