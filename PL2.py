import gurobipy as gb

def PL2(Qtype1, Qtype2, gG, gC):
    PL2 = gb.Model("PL2")
    
    #============================================VARIABLES
    repartition = [] 
    q11 = PL2.addVar(lb = 0 ,vtype = gb.GRB.INTEGER, name='q11')
    q12 = PL2.addVar(lb = 0 ,vtype = gb.GRB.INTEGER, name='q12')
    q21 = PL2.addVar(lb = 0 ,vtype = gb.GRB.INTEGER, name='q21')
    q22 = PL2.addVar(lb = 0 ,vtype = gb.GRB.INTEGER, name='q22')
    
    #============================================CONSTRAINTS
    PL2.addConstr(q11 + q12 <= Qtype1, "Quantité en type 1")
    PL2.addConstr(q21 + q22 <= Qtype2, "Quantité en type 2")
    PL2.addConstr((10*q11 + 5*q21) >= 8*(q11+q21), "Contrainte de qualité Gazoline")
    PL2.addConstr((10*q12 + 5*q22) >= 6*(q12+q22), "Contrainte de qualité Gaz de Chauffage")
    
    #============================================SOLVE
    Income = gG*(q11+q21) + gC*(q12+q22)
    PL2.setObjective(Income, gb.GRB.MAXIMIZE)
    PL2.optimize()
    
    vars = PL2.getVars()
    for var in vars:
        print(var.varName, var.x)
    
    print(f'Resultant en un profit de {PL2.ObjVal} Dt')
    
PL2(5000, 10000, 24.8, 19.9)