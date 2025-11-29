import numpy as np
import gurobipy as gp
from gurobipy import GRB


# fonction permettant de generer une grille 
# taille M, N avec P obstacles
def generer_grille_lp(M, N, P, seed=None):

    if seed is not None:
        np.random.seed(seed)
    coefficients = np.random.randint(0, 1001, size=(M, N))

    m = gp.Model("grille_obstacles")
    m.Params.OutputFlag = 0  

    x = m.addVars(M, N, vtype=GRB.BINARY, name="x")

    m.setObjective(
        gp.quicksum(coefficients[i, j] * x[i, j] for i in range(M) for j in range(N)),
        GRB.MINIMIZE
    )

    m.addConstr(
        gp.quicksum(x[i, j] for i in range(M) for j in range(N)) == P,
        name="total_obstacles"
    )

    for i in range(M):
        m.addConstr(
            gp.quicksum(x[i, j] for j in range(N)) <= 2 * P / M,
            name=f"max_ligne_{i}"
        )

    for j in range(N):
        m.addConstr(
            gp.quicksum(x[i, j] for i in range(M)) <= 2 * P / N,
            name=f"max_col_{j}"
        )

    for i in range(M):
        for j in range(1, N - 1):
            m.addConstr(
                x[i, j-1] + x[i, j+1] - x[i, j] <= 1,
                name=f"no_101_ligne_{i}_{j}"
            )

    for j in range(N):
        for i in range(1, M - 1):
            m.addConstr(
                x[i-1, j] + x[i+1, j] - x[i, j] <= 1,
                name=f"no_101_col_{i}_{j}"
            )

    m.optimize()

    if m.status != GRB.OPTIMAL:
        raise RuntimeError("Pas de solution")


    obstacles = np.zeros((M, N), dtype=int)
    for i in range(M):
        for j in range(N):
                obstacles[i, j] = x[i, j].X 

    return coefficients, obstacles


M, N = 9, 10
P = 20
c, mat = generer_grille_lp(M, N, P,seed=0)

print("Poids :")
print(c)
print("\nObstacles :")
print(mat)
