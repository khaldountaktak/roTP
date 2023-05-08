import numpy as np
import gurobipy as gp 

def planification(x1,x2,x3,x4,x5,x6,x7):
    #===================INITILISATION
    jours=[x1,x2,x3,x4,x5,x6,x7]
    jour = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
    mat=np.ones((7,7),dtype=int)
    for c in range(7):
        i = c+5
        mat[i%7,c] = 0
        mat[(i+1)%7,c] = 0
    
    #===================MODEL
    PL3 = gp.Model("PL3")
    x=[]
    for i in range(7):
        x.append(PL3.addVar(lb = 0 ,vtype = gp.GRB.INTEGER, name='x'+str(i+1) ) )
    X = np.array(x)
    X = X.reshape((1,7))
    for j in range(7):
        PL3.addConstr(gp.quicksum(mat[j,:] * x) >= jours[j],"Nbre d'employé min requis pour " + jour[j]+" est "+str(jours[j]))

    PL3.setObjective( gp.quicksum(x)  ,gp.GRB.MINIMIZE)

    PL3.optimize()    
      
    #===================PLANIFICATION
    aux=[]
    for i in range(7):
        aux.append(int(x[i].x))
    result=[]
    for i in range(7):
       result.append(aux[(i+2)%7])
    print("plannification des congés ")
    
    for i in range(7):
        print (jour[i]+"  :"+str(result[i] ))
    
    #===================RESOLUTION
    print ("le nombre totale optimale des employés est ",int(PL3.objVal))
    return result,PL3.objVal
        
planification(17,13,15,19,14,16,11) 