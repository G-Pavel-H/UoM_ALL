import sys
from timeit import default_timer as timer
from knapsack import knapsack

class dp(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        
    def DP(self, solution):
        # Renaming things to keep track of them wrt. names used in algorithm
        values = self.item_values
        weights = self.item_weights
        N = self.Nitems
        C = self.Capacity
        
        # the dynamic programming function for the knapsack problem
        # the code was adapted from p17 of http://www.es.ele.tue.nl/education/5MC10/solutions/knapsack.pdf

        # v array holds the valuesues / profits / benefits of the items
        # wv array holds the sizes / weights of the items
        # n is the total number of items
        # W is the constraint (the weight capacity of the knapsack)
        # solution: True in position n means pack item number n+1. False means do not pack it.
        
        # V and Keep should be 2d arrays for use in the dynamic programming solution
        # The are both of size (n + 1)*(W + 1)
        
        # Initialise V and keep
        # ADD CODE HERE

        V = [[0 for col in range(C+1)] for row in range(N+1)]
        keep = [[0 for col in range(C+1)] for row in range(N+1)]

        for x in range(C+1):
            V[0][x] = 0

        for i in range(1, N+1):
            for j in range(C+1):
                if weights[i]  <= j and (values[i] + V[i-1][j-weights[i]] > V[i-1][j]):
                    V[i][j] = values[i] + V[i-1][j-weights[i]]
                    keep[i][j] = 1
                else:
                    V[i][j] = V[i-1][j]
                    keep[i][j] = 0
        K = C
        for i in range(N, 0, -1):
            if keep[i][K] == 1:
                solution[i] = True
                K -= weights[i]

        

        print("Nitems: ", N)
        print("Capacity: ", C)
        self.QUIET = False
        print("Finished.\nPack the following items for optimal")
        self.check_evaluate_and_print_sol(solution)

    
        
knapsk = dp(sys.argv[1])
solution = [False]*(knapsk.Nitems + 1)
start = timer()
knapsk.DP(solution)
end = timer()
print("Time: ", end-start)
knapsk.check_evaluate_and_print_sol(solution)
