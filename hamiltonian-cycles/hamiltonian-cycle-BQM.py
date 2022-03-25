# -*- coding: utf-8 -*-
"""
 File name: hamiltonian-cycle-BQM.py
 
 File type: Python file
 
 Author: Jorge Luis Hita
 
 Institution: Private use
              
 Date: 25th January 2022

 Description: This program solves naïve instances of the Hamiltonian cycle 
     problem using D-Wave's Quantum Annealer.

     A Hamiltonian cycle problem is a problem of visiting every node in a 
     graph, subject to the restriction that every node should be visited once
     and only once.

     When the graph is complete, the solution is easier than in the general
     case. 

     In this file, the Binary Quadratic Model sampler (BQM) is used.

Disclaimer: This code is an experimental, not-optimized, not-tested code.
     USE IT AT YOUR OWN RISK.

"""

import numpy as np
import pandas as pd

from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

def main():

    # Define the number of nodes to visit
    n_nodes = 5
    # Defines the order in which each node is visited
    n_order = n_nodes
    # Defines the lagrange multipliers for the constraints
    lag_mul_1 = 1
    lag_mul_2 = 1

    # Defines the array of binary variables
    x = [[f'x_c_{node}_p_{order}' for order in range(n_order)] for node in range(n_nodes)]

    # Declares the bqm object
    bqm = BinaryQuadraticModel('BINARY')

    # Define the constraint 1: Any node must be visited once and only once
    for node in range(n_nodes):
        c_weights = [(x[node][order], 1) for order in range(n_order)]
        bqm.add_linear_equality_constraint(c_weights, constant=-1, lagrange_multiplier=lag_mul_1)

    # Define the constraint 2: Any order must be selected once and only once
    for order in range(n_order):
        c_weights = [(x[node][order], 1) for node in range(n_nodes)]
        bqm.add_linear_equality_constraint(c_weights, constant=-1, lagrange_multiplier=lag_mul_2)

    # Declare the sample to be used and solve the problem
    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm, num_reads=100)

    # Take best solution
    first_sample = sampleset.first.sample

    # Reshapes the best solution
    data = np.zeros((n_nodes, n_order))
    for order in range(n_order):
        for node in range(n_nodes):
            data[node, order] = first_sample[x[node][order]]

    # Defines column and row names for the final solution
    columns = ['order_'+str(order) for order in range(n_order)]
    index = ['node_'+str(node) for node in range(n_nodes)]
    df_solution = pd.DataFrame(data=data, columns=columns, index=index)

    # Prints final solution
    print(df_solution)
    
	
if __name__=="__main__":
    main()
