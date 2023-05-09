import gurobipy as gp

class PL1:
    def __init__(self,Rendement,Prix_vente,main_doeuvre,Temps_machine,Eau,Salaire_annuel,Frais_gestion,prix_main_doeuvre,eau_dirrigation,heure_machine):
        self.Rendement = Rendement
        self.Prix_vente = Prix_vente
        self.main_doeuvre = main_doeuvre
        self.Temps_machine = Temps_machine
        self.Eau = Eau
        self.Salaire_annuel = Salaire_annuel
        self.Frais_gestion = Frais_gestion
        self.prix_main_doeuvre = prix_main_doeuvre
        self.eau_dirrigation = eau_dirrigation
        self.heure_machine = heure_machine
        self.names= ["Blé", "Orge", "Maïs", "Bet-sucre", "Tournesol"]

    def run(self):
        model = gp.Model("PL1")

        # Variables de décision : quantité de chaque culture à planter
        x = model.addVars(range(5), vtype=gp.GRB.INTEGER, name="x")

        # Fonction d'objective
        model.setObjective(gp.quicksum( x[i] * (
                                ( self.Rendement[i]*self.Prix_vente[i] )
                                - ( self.main_doeuvre[i]*self.Salaire_annuel[i] )
                                - ( self.Temps_machine[i]*30 )
                                - ( self.Eau[i]*0.1 )
                            ) - self.Frais_gestion[i]
                            for i in range(5)),gp.GRB.MAXIMIZE)

        # Contraintes
        model.addConstr(gp.quicksum( (self.main_doeuvre[i]*x[i]) for i in range(5)) <= self.prix_main_doeuvre)
        model.addConstr(gp.quicksum( (self.Temps_machine[i]*x[i]) for i in range(5)) <= self.heure_machine)
        model.addConstr(gp.quicksum( (self.Eau[i]*x[i]) for i in range(5)) <= self.eau_dirrigation)
        for i in range(5):
            model.addConstr(x[i] >= 0)
        model.addConstr(gp.quicksum( x[i] for i in range(5)) <= 1000)

        # Resolution
        model.optimize()

        # Affichage des resultats
        resultat = ""
        for i,v in enumerate(model.getVars()):
            resultat += '%s: %g\n--------------\n' % (self.names[i], v.x)

        return resultat

if "__main__" == __name__:
    # Parametres du probleme
    Rendement = [75,60,55,50,60]
    Prix_vente = [60,50,66,110,60]
    main_doeuvre = [2,1,2,3,2]
    Temps_machine = [30,24,20,28,25]
    Eau = [3000,2000,2500,3800,3200]
    Salaire_annuel = [500,500,600,700,550]
    Frais_gestion = [250,180,190,310,320]

    # Valeurs des contraintes
    prix_main_doeuvre = 3000
    eau_dirrigation = 25000000
    heure_machine = 24000

    pl1 = PL1(Rendement=Rendement,Prix_vente=Prix_vente,main_doeuvre=main_doeuvre,Temps_machine=Temps_machine,
              Eau=Eau,Salaire_annuel=Salaire_annuel,Frais_gestion=Frais_gestion,prix_main_doeuvre=prix_main_doeuvre,
              eau_dirrigation=eau_dirrigation,heure_machine=heure_machine)
    
    print(pl1.run())