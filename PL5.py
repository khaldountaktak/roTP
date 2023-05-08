import gurobipy as gb 

def PL5():
    Offre = [35,50,40]
    Demande = [45,20,30,30]
    
    Couts = [[8,6,10,9],
            [9,12,13,7],
            [14,9,16,5]]
    
    PL5 = gb.Model("PL5")
    Q = [[PL5.addVar(vtype=gb.GRB.CONTINUOUS, name='q'+str(i+1)+str(j+1)) for i in range(4)] for j in range(3)]
    
    for i in range(4):
        PL5.addConstr(sum(Q[j][i] for j in range(3)) >= Demande[i])    
    
    for j in range(3):
        PL5.addConstr(sum(Q[j][i] for i in range(4)) <= Offre[j])
        
    Cout = sum(Q[i][j]*Couts[i][j]*(10**6) for i in range(3) for j in range(4))
    PL5.setObjective(Cout, gb.GRB.MINIMIZE)
    
    PL5.optimize()
    
    vars = PL5.getVars()
    for var in vars:
        print(var.varName, var.x)
    
    print(f'Avec un cout minimale de {int(PL5.ObjVal)}')

PL5()