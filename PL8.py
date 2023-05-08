import gurobipy as gp
import numpy as np

class PL8:
    def __init__(self,costs):
        self.costs = costs

    def run(self):
        # Création du modèle
        model = gp.Model("PL8")

        # Variables de décision : binaire indiquant si un arc est utilisé ou non
        x = model.addVars(range(10), range(10), vtype=gp.GRB.BINARY, name="x")

        # Fonction objectif : minimiser la somme des coûts des arcs utilisés
        model.setObjective(gp.quicksum(self.costs[i][j] * x[i,j] for i in range(10) for j in range(10) if not np.isnan(self.costs[i][j])), gp.GRB.MINIMIZE)

        # Contrainte
        # Noeud debut
        model.addConstr(gp.quicksum( x[1,j] for j in range(1,4) ) == 1)
        # Noeud fin
        model.addConstr(gp.quicksum( x[i,9] for i in range(4,9) if (i!=7) ) == 1)

        # Les parametres nulles doievent rester nulles
        for i in range(10):
            for j in range(10):
                if np.isnan(self.costs[i][j]):
                    model.addConstr(x[i,j] == 0)

        for k in range(1, 9):
            model.addConstr(gp.quicksum(x[i,k] for i in range(10) if self.costs[i-1][k-1] != 0) == gp.quicksum(x[k,j] for j in range(10) if self.costs[k-1][j-1] != 0))

        # Résolution du modèle
        model.optimize()
        
        # create matrix that takes 10*10 values of v.x
        matrix = np.zeros((10,10),dtype=int)
        tab = []
        for i,v in enumerate(model.getVars()):
            tab.append(v.x)

        # fill the matrix with the values of tab
        for i in range(10):
            for j in range(10):
                if tab[i*10+j] > 0:
                    matrix[i][j] = int(tab[i*10+j])

        resultat = ""
        chemin = []
        # Affichage de la solution
        if model.status == gp.GRB.OPTIMAL:
            for i in range(10):
                for j in range(10):
                    if matrix[i][j] == 1:
                        resultat += "Chemin de {} à {} : {}".format(i+1,j+1,self.costs[i][j]) + "\n"
                        chemin.append("{}".format(i+1))
            resultat += "Coût total : {}".format(model.objVal) + "\n"
            resultat += "Meilleur chemin: "

            for i in range(len(chemin)-1):
                resultat += chemin[i] + " -> "
            resultat += chemin[-1] + " -> 10"
        else:
            print("Pas de chemin optimal!")
        return resultat


if "__main__" == __name__:
    # Données d'entrée : matrice des coûts entre chaque ville
    costs = [
        [np.nan, 70, 63, 56, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        [np.nan, np.nan, 25, 19, 73, 50, 79, np.nan, np.nan, np.nan],
        [np.nan, 25, np.nan, 29, 69, 61, np.nan, np.nan, np.nan, np.nan],
        [np.nan, 19, 29, np.nan, 67, 45, np.nan, np.nan, 85, np.nan],
        [np.nan, np.nan, np.nan, np.nan, np.nan, 18, 67, 69, 54, 87],
        [np.nan, np.nan, np.nan, np.nan, 18, np.nan, 72, 52, 51, 97],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 17, 31, 72],
        [np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, 17, np.nan, 15, np.nan],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 31, 15, np.nan, 69],
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, np.nan]
    ]

    pl8 = PL8(costs)
    print(pl8.run())