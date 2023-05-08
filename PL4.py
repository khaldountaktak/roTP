import gurobipy as gp

class PL4:
    def __init__(self,C,Cs,D,Sal,Hsup,R,L,h,H,Hmax):
        self.C = C
        self.Cs = Cs
        self.D = D
        self.Sal = Sal
        self.Hsup = Hsup
        self.R = R
        self.L = L
        self.h = h
        self.H = H
        self.Hmax = Hmax

    def run(self):
        # Modèle d'optimisation
        model = gp.Model()

        # Variables de décision
        NHS = model.addVars(range(4), vtype=gp.GRB.INTEGER, lb=0, name="NHS")  # Nombre d'heures supplémentaires par mois
        NCH = model.addVars(range(4), vtype=gp.GRB.INTEGER, lb=0, name="NCH")  # Nombre de paires de chaussures fabriquées par mois
        NOR = model.addVars(range(4), vtype=gp.GRB.INTEGER, lb=0, name="NOR")  # Nombre d'ouvriers recrutés par mois
        NOL = model.addVars(range(4), vtype=gp.GRB.INTEGER, lb=0, name="NOL")  # Nombre d'ouvriers licenciés par mois
        S = model.addVars(range(5), vtype=gp.GRB.INTEGER, lb=0, name="S")  # Stock de paires de chaussures par mois
        NO = model.addVars(range(5), vtype=gp.GRB.INTEGER, lb=0, name="NO")  # Nombre d'ouvriers disponibles par mois

        # Fonction objectif
        obj = (gp.quicksum(self.Cs * S[i] for i in range(5))
            + gp.quicksum(self.Sal * NO[i] for i in range(5))
            + gp.quicksum(self.Hsup * NHS[i] for i in range(4))
            + gp.quicksum(self.R * NOR[i] for i in range(4))
            + gp.quicksum(self.L * NOL[i] for i in range(4))
            + gp.quicksum(self.C * NCH[i] for i in range(4)))
        model.setObjective(obj, sense=gp.GRB.MINIMIZE)

        # Contraintes

        # Les heures supplémentaires
        for i in range(4):
            model.addConstr(NHS[i] <= 20 * NO[i])

        # La production & la demande
        model.addConstr(S[0] + NCH[0] >= 3000)
        model.addConstr(S[1] + NCH[1] >= 5000)
        model.addConstr(S[2] + NCH[2] >= 2000)
        model.addConstr(S[3] + NCH[3] >= 1000)

        # La production & les heures de travail
        for i in range(4):
            model.addConstr(NCH[i] <= (1/4) * (NHS[i] + NO[i] * 160))

        # Effectif
        model.addConstr(NO[0] == 100)
        for i in range(3):
            model.addConstr(NO[i+1] == NO[i] + NOR[i] - NOL[i])

        # Stock
        model.addConstr(S[0] == 500)
        model.addConstr(S[1] == S[0] + NCH[0] - 3000)
        model.addConstr(S[2] == S[1] + NCH[1] - 5000)
        model.addConstr(S[3] == S[2] + NCH[2] - 2000)
        model.addConstr(S[4] == S[3] + NCH[3] - 1000)

        # Optimisation
        model.optimize()

        # Affichage des résultats
        print("Solution optimale:")
        for i in range(4):
            print("NHS[{}] = {}".format(i, int(NHS[i].x)))
            print("NCH[{}] = {}".format(i, int(NCH[i].x)))
            print("NOR[{}] = {}".format(i, int(NOR[i].x)))
            print("NOL[{}] = {}".format(i, int(NOL[i].x)))
            print("S[{}] = {}".format(i, int(S[i].x)))
            print("NO[{}] = {}".format(i, int(NO[i].x)))

        # # Signe
        # for i in range(4):
        #     model.addConstr(S[i] >= 0)
        #     model.addConstr(NO[i] >= 0)
        #     model.addConstr(NOR[i] >= 0)
        #     model.addConstr(NOL[i] >= 0)
        #     model.addConstr(NHS[i] >= 0)



if "__main__" == __name__:
    # Données du problème
    C = 15  # Coût de production d'une paire de chaussure par mois
    Cs = 3  # Coût de stockage d'une paire de chaussure par mois
    D = [0, 3000, 5000, 2000, 1000]  # Demande de paires de chaussures par mois
    Sal = 1500  # Salaire d'un ouvrier par mois
    Hsup = 13  # Coût d'une heure supplémentaire par ouvrier
    R = 1600  # Frais de recrutement d'un ouvrier
    L = 2000  # Frais de licenciement d'un ouvrier
    h = 1  # Nombre d'heures nécessaires pour fabriquer une paire de chaussure
    H = 160  # Volume horaire mensuel de travail par ouvrier
    Hmax = 20  # Nombre d'heures supplémentaires max par ouvrier

    pl4 = PL4(C,Cs,D,Sal,Hsup,R,L,h,H,Hmax)
    pl4.run()