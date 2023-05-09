import gurobipy as gp

def PL6():
    C=[
        [0,5,3,5,5,20,20],
        [9,0,9,1,1,8,15],
        [0.4,8,0,1,0.5,10,12],
        [0,0,0,0,1.2,2,12],
        [0,0,0,0.8,0,2,12],
        [0,0,0,0,0,0,1],
        [0,0,0,0,0,7,0]
    ]
    
    X=[
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    PL6=gp.Model("PL6")
    
    for i in range(7):
        for j in range(7):
            X[i][j]=PL6.addVar(vtype=gp.GRB.INTEGER ,name='X'+str(i+1)+str(j+1))
    
    PL6.setObjective(sum(X[i][j]*C[i][j] for i in range(7) for j in range(7)),gp.GRB.MINIMIZE)
    
    PL6.addConstr(sum(X[0][j] for j in range(7))<=200)
    PL6.addConstr(sum(X[1][j] for j in range(7))<=300)
    PL6.addConstr(sum(X[2][j] for j in range(7))<=100)
    
    PL6.addConstr(sum(X[i][5] for i in range(7)) - X[5][6] == 400)
    PL6.addConstr(sum(X[i][6] for i in range(7)) - X[6][5] == 180)
    
    for i in range(7):
        for j in range(7):
            PL6.addConstr( X[i][j] <= 200)
    
    for i in range(7):
        for j in range(7):
            PL6.addConstr( X[i][j] >= 0)
            
    PL6.addConstr(sum(X[3][j] for j in range(7)) <= sum(X[i][3] for i in range(7)))
    PL6.addConstr(sum(X[4][j] for j in range(7)) <= sum(X[i][4] for i in range(7)))
    
    PL6.optimize()
    
    vars = PL6.getVars()
    for var in vars:
        print(var.varName, var.x)
    
    print(f'Le cout optimal de transportation de la production est de {PL6.ObjVal} Dt')
        
PL6()