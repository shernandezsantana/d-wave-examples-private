from dwave_qbsolv import QBSolv
import numpy as np
import pandas as pd

def main():

    # Define the number of nodes to visit
    n_nodes = 5
    # Defines the order in which each node is visited
    n_order = n_nodes

    # Calculamos los valores de los coeficientes h y J que necesitamos para definir el problema QUBO
    B = 1
    A = 1.5 * B

    J = {}
    h = {}
    bias = 0.0


    for eli in range(0, n_order*n_nodes):
        # all h are 0, from 0 to n_orders*n_nodes
        h[eli] = 0
        for elj in range(eli, n_order*n_nodes):
            #if eli!=elj:
            # J elements set to 0, if i,j belong to upper triangle
            J[(eli, elj)] = 0.0

    # J elements are 2A in all diagonal elements in the off-diagonal squares 5x5 in
    # the upper triangle. each square corresponds to a node, so doing this adds a
    # penalty of  2 when two consecutive nodes (nodei, nodei+1) have the same 
    # order.
    for eli in range(0, n_nodes-1, 1):
        for elj in range(eli+1, n_nodes, 1):
            for elci in range(n_order):
                J[(elci + eli*n_order, elci + elj*n_order)] += 2.0*A# * distances[eli, elj]

    # J elements are 2A in all the upper triangles of all the 5x5 blocks, that is, 
    # for the same node. This gives a penalty to having one single node with two 
    # different orders.
    for eli in range(n_nodes):
        for elic in range(0, n_order-1, 1):
            for eljc in range(elic+1, n_order, 1):
                J[(elic + eli*n_order, eljc + eli*n_order)] += 2.0 * A


    # h elements are 2(1-2)A for all (n_orders*n_nodes variables)
    for elc in range(n_order):     
        for eli in range(0, n_nodes):
            h[eli + elc*n_nodes] += 2*A*(1.0 - 2.0)  # 1 comes cause x_i*x_i=x_i

    # sum as many 2A as number of nodes for bias, that is, bias = 2*A*n_nodes
    for eli in range(n_nodes):
        bias += 2*A

    # obtain Q
    Q = J.copy()

    for elc in range(n_order):     
        for eli in range(n_nodes):
            Q[(eli + elc*n_nodes, eli + elc*n_nodes)] += h[eli + elc*n_nodes]

    response = QBSolv().sample_qubo(Q)
    print("samples=" + str(list(response.samples())))
    print("energies=" + str(list(response.data_vectors['energy'])))

    data = np.zeros([n_nodes, n_order])
    for node in range(n_nodes):
        for order in range(n_order):
            data[node, order] = response.samples()[0][order+node*n_order]


    # Defines column and row names for the final solution
    columns = ['order_'+str(order) for order in range(n_order)]
    index = ['node_'+str(node) for node in range(n_nodes)]
    df_solution = pd.DataFrame(data=data, columns=columns, index=index)

    # Prints final solution
    print(df_solution)


if __name__=="__main__":
    main()