from itertools import chain, combinations
from pulp import LpVariable, LpProblem, lpSum, value, LpMaximize, LpStatus


# everything is zero-index based
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def nash_social_welfare_maximization(values1, values2):
    m = len(values1)

    # Generate all possible partitions of m items into two sets
    all_partitions = list(powerset(range(m)))

    max_welfare = float('-inf')
    max_partition = None

    # Iterate through all partitions and find the one with maximum welfare
    for partition in all_partitions:
        bundle1 = set(partition)
        bundle2 = set(range(m)) - bundle1

        welfare = sum(values1[i] for i in bundle1) * sum(values2[j] for j in bundle2)
        print(bundle1, welfare)
        print('*****')

        if welfare > max_welfare:
            max_welfare = welfare
            max_partition = (list(bundle1), list(bundle2))

    print(max_welfare)
    return max_partition

def create_linear_program(V, target):
    m = len(V)

    # Create LP problem
    lp_problem = LpProblem("Feasibility_Check", LpMaximize)

    # Decision variables
    a = [LpVariable(f"a_{i}", lowBound=0) for i in range(1, m + 1)]

    all_partitions = list(powerset(range(m)))
    target_prime = set(range(m)) - set(target)
    lhs = lpSum([a[i] for i in target]) * lpSum([V[j] for j in target_prime])
    lp_problem += lpSum(a) == 1
    eps = 0.001
    for partition in all_partitions:
        if set(partition) == set(target):
            continue
        bundle = set(partition)
        bundle_prime = set(range(m)) - bundle
    # Constraints
        rhs = lpSum([a[i] for i in bundle]) * lpSum([V[j] for j in bundle_prime]) + eps
        lp_problem += lhs >= rhs

    return lp_problem

def check_feasibility(V, target):
    lp_problem = create_linear_program(V, target)
    print(lp_problem)

    # Solve the linear program
    lp_problem.solve()

    # Check feasibility
    if LpStatus[lp_problem.status] == 'Optimal':
        print("Feasible")
        lst = []
        for var in lp_problem.variables():
            if var.name.startswith('a_'):
                print(f"{var.name} = {var.varValue}")
                lst.append(var.varValue)
        return lst
    else:
        print("Infeasible")

def NSW_max_driver(values1, values2):
    # Example usage
    # values1 = [0.1, 0.2, 0.3, 0.4]
    # values2 = [0.1, 0, 0.4, 0.5]

    allocation = nash_social_welfare_maximization(values1, values2)
    print("Nash Social Welfare Maximizing Allocation:")
    print("Bundle 1:", allocation[0])
    print("Bundle 2:", allocation[1])


lst = check_feasibility([0.1,0.2,0.3,0.4], [1,3])
# check_feasibility([0.25 * element for element in [1,1,1,1]], [1,3,2])
NSW_max_driver([0.1,0.2,0.3,0.4],lst)

