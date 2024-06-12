#!/usr/bin/env python3
from constraint import Problem , AllDifferentConstraint, ExactSumConstraint
#print(solns)

#solns= problem.getSolutions() 
#print(solns)


# Task 1    
def Travellers(List):
    problem= Problem()

    people= ["claude", "olga", "pablo", "scott"]
    times= ["2:30", "3:30", "4:30", "5:30"] 
    destinations= ["peru", "romania", "taiwan", "yemen"]

    t_variables= list(map(lambda x: "t_"+x, people)) 
    d_variables= list(map(lambda x: "d_"+x, people))

    problem.addVariables(t_variables , times) 
    problem.addVariables(d_variables , destinations)
    problem.addConstraint(AllDifferentConstraint(),t_variables) 
    problem.addConstraint(AllDifferentConstraint(),d_variables)

    #adding the normal constraints
    for person in people: 
        #problem.addConstraint((lambda x,y,z: (y != "yemen") or ((x == "4:30") and (z == "2:30")) or ((x == "5:30") and (z == "3:30"))), ["t_"+person , "d_"+person , "t_olga"])
        problem.addConstraint((lambda x: ((x == "3:30") or (x == "2:30"))), ["t_claude"])
        problem.addConstraint((lambda x,y: (y != "peru") or ((x == "2:30") and (y == "peru"))),["t_"+person, "d_"+person])
        problem.addConstraint((lambda x,y: ((x != "taiwan") and (x!="yemen")) or ((x == "taiwan") and (y == "5:30")) or ((x == "yemen") and (y == "4:30"))), ["d_" + person, "t_" + person])
        problem.addConstraint((lambda x,y: (x != "yemen") and (y != "2:30") and (y!="3:30")), ["d_pablo", "t_pablo"])
    

    #adding the special constraint      
    for i in List:
        problem.addConstraint((lambda x, i=i: x == i[1]), ["t_"+ i[0]])

    result = problem.getSolutions()
    return result

#print(Travellers([["olga", "2:30"],["scott","4:30"]]))

# Task 2
def CommonSum(n):
    #I have found the formula by trying different examples of different sizes.
    #The formula is the following: N(N2+1)/2
    #Where N is the size of the magic square.
    value = n*((n**2)+1)/2
    return value 
  
# Task 3
def msqList(n, pairList):
    problem = Problem() 
    problem.addVariables(range(0,n*n), range(1,n*n+1))
    problem.addConstraint(AllDifferentConstraint(), range(0,n*n))

    #checkign row
    for row in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)), [row * n + i for i in range(n)])
    #checking col
    for col in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)), [col + n * i for i in range(n)])
    #checking diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in range(0, n**2, n+1)])
    #checking other diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in range(n**2-n, 0, -(n-1))])
    
    for i in pairList:
        problem.addConstraint((lambda x, i=i: x == i[1]), [i[0]])

    
    sol = problem.getSolutions()
    #print(sol)
    return sol

#msqList(4,[[0,13],[1,12],[2,7]])

# Task 4
def pmsList(n, pairList):
    first_pos = [1, n, (n**2)-2, (n**2)-n-1]
    second_pos = [n-2, 2*n-1, (n**2)-2*n, (n**2)-n+1]

    problem = Problem() 
    problem.addVariables(range(0,n*n), range(1,n*n+1))
    problem.addConstraint(AllDifferentConstraint(), range(0,n*n))

    #checkign row
    for row in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)), [row * n + i for i in range(n)])
    #checking col
    for col in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)), [col + n * i for i in range(n)])
    #checking diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in range(0, n**2, n+1)])
    #checking diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in range(n**2-n, 0, -(n-1))])
    #first broken diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in first_pos])
    #second broken diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i for i in second_pos])

    for i in pairList:
        problem.addConstraint((lambda x, i=i: x == i[1]), [i[0]])

    sol = problem.getSolutions()

    # print(sol)
    return sol

#pmsList(4,[[0,13],[1,12],[2,7]])

# Debug
if __name__ == '__main__':
    print("debug run...")

