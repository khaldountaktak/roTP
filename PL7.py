import gurobipy as gp
import numpy as np

class PL7:
    def __init__(self,costs):
        self.costs = costs
        self.num_companies = len(costs)
        self.num_projects = len(costs[0])

    def run(self):
        # Creation du model
        model = gp.Model("PL7")

        # Variables de decision
        x = model.addVars(self.num_companies, self.num_projects, vtype=gp.GRB.BINARY, name="x")

        # Fonction d'objective
        model.setObjective(gp.quicksum(self.costs[i][j] * x[i, j] for i in range(self.num_companies) for j in range(self.num_projects) if not np.isnan(self.costs[i][j])), gp.GRB.MINIMIZE)

        # Add constraints
        # Une seule entreprise par projet
        for j in range(self.num_projects):
            model.addConstr(gp.quicksum(x[i, j] for i in range(self.num_companies) if not np.isnan(self.costs[i][j])) == 1)
        # Au max 2 projets par entreprise
        for i in range(self.num_companies):
            model.addConstr(gp.quicksum(x[i, j] for j in range(self.num_projects) if not np.isnan(self.costs[i][j])) <= 2)

        # Optimisation
        model.optimize()

        # Affichage des résultats
        if model.status == gp.GRB.Status.OPTIMAL:
            resultat = ""
            assignment = []
            for i in range(self.num_companies):
                for j in range(self.num_projects):
                    if not np.isnan(self.costs[i][j]) and x[i, j].x > 0.5:
                        assignment.append((i+1, j+1))
            if assignment:
                for i, j in assignment:
                    resultat += f"Assigner le project {j} a l'entreprise {i}\n"
                resultat += "Valeur objective:"+ str(model.objVal)
            else:
                resultat += "Aucune solution trouve."
            return resultat

couts = [
     [np.nan, 8200, 7800, 5400, np.nan, 3900, np.nan, np.nan],
      [7800, 8200, np.nan, 6300, np.nan, 3300, 4900, np.nan],
     [np.nan, 4800, np.nan, np.nan, np.nan, 4400, 5600, 3600],
      [np.nan, np.nan, 8000, 5000, 6800, np.nan, 6700, 4200],
     [7200, 6400, np.nan, 3900, 6400, 2800, np.nan, 3000],
      [7000, 5800, 7500, 4500, 5600, np.nan, 6000, 4200]
  ]

pl7 = PL7(couts)
print(pl7.run())