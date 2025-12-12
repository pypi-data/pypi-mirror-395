from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 

import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.optimize import minimize
from matplotlib.ticker import FuncFormatter

class Object:
    def __init__(self):
        self.Timestamp=None

        #Input and Output Connector
        self.Inlet=FluidPort() 
        self.Outlet=FluidPort()

        # #Input Data
        self.eta=None
        self.Pdischarge_bar=None
        # self.Tcond_degC=None
        self.Pdischarge=None #self.Pdischarge_bar*100000
        # self.Tdischarge_target=None #°C

        #points de fonctionnement de la pompe
        self.X_F = None #débit volumique m3/h X_F = [5,34,40,50]
      
        self.Y_hmt = None # Hauteur manométrique Y_hmt = [12,60,80,68]
        self.Y_eta = None # point de rendement Y_eta = [0.4,0.8,0.9,0.1]

        # Modèles et données pour la courbe
        self.model_hmt = None
        self.model_eta = None
        self.polynomial_features = None
        self.nb_degree = None
        self.x_new_min = None
        self.x_new_max = None
        self.Y_hmt_NEW = None
        self.Y_eta_NEW = None

        # #Initial Values
        #self.Inlet.fluid=None
        # self.Inlet.P=101325
        # self.F=0.1
        # self.Inlet.F=self.F

        # self.F_Sm3s=None
        # self.F_Sm3h=None
        self.F_Sm3s=None
        
        #Output Data
        self.df=[]

        self.Q_pump=0
    #     self.Q_losses=0
        self.Ti_degC=None
        
        # Callback pour détecter les changements de pression en aval
        self.Outlet.callback = self.on_pressure_change
        
    def on_pressure_change(self):
        """
        Callback appelé lorsque self.Outlet.P change (pression imposée par le réseau en aval).
        Recalcule le débit de la pompe en fonction de la nouvelle pression de refoulement.
        """
        if hasattr(self, '_calculating') or hasattr(self, '_calculating_inverse'):
            return  # Éviter les boucles infinies pendant le calcul
        
        print(f"🔄 PUMP CALLBACK: Détection changement pression Outlet: {self.Outlet.P/100000:.3f} bar")
        
        # Si la pression de sortie change, recalculer le point de fonctionnement
        if self.Outlet.P is not None and self.Inlet.P is not None:
            self._calculating_inverse = True
            try:
                self.calculate_from_network_pressure()
            finally:
                delattr(self, '_calculating_inverse')
    
    def calculate_from_network_pressure(self):
        """
        Recalcule le débit de la pompe en fonction de la pression imposée par le réseau.
        Appelée automatiquement via callback quand Outlet.P change.
        """
        if self.model_hmt is None:
            print("⚠️  Modèle HMT non initialisé. Impossible de recalculer le débit.")
            return
        
        # Calculer le nouveau delta_P imposé par le réseau
        self.delta_p = self.Outlet.P - self.Inlet.P
        
        # Calculer la HMT correspondante
        rho = PropsSI("D", "P", self.Inlet.P, "T", self.Ti_degC + 273.15, self.Inlet.fluid)
        g = 9.81
        self.hmt = self.delta_p / (rho * g)
        
        print(f"   ΔP réseau: {self.delta_p/100000:.3f} bar → HMT: {self.hmt:.2f} m")
        
        # Trouver le débit correspondant sur la courbe caractéristique
        def error_function(F_m3h):
            F_m3h_array = np.array(F_m3h).reshape(-1, 1)
            F_transformed = self.polynomial_features.transform(F_m3h_array)
            hmt_predicted = self.model_hmt.predict(F_transformed)[0][0]
            return abs(hmt_predicted - self.hmt)
        
        # Recherche du débit
        initial_guess = self.F_m3h if self.F_m3h is not None else self.X_F[0]
        bounds = [(0.1, 1.5 * max(self.X_F))]
        
        result = minimize(
            error_function,
            x0=initial_guess,
            bounds=bounds,
            method='L-BFGS-B',
            options={'ftol': 1e-6, 'disp': False}
        )
        
        if result.success:
            old_F_m3h = self.F_m3h
            self.F_m3h = result.x[0]
            
            # Recalculer le débit massique
            self.F_m3s = self.F_m3h / 3600
            self.Inlet.F = self.F_m3s * rho
            self.Outlet.F = self.Inlet.F
            
            # Recalculer le rendement
            self.calculate_eta()
            
            print(f"   ✓ Débit adapté: {old_F_m3h:.2f} → {self.F_m3h:.2f} m³/h (F={self.Inlet.F:.4f} kg/s)")
            print(f"   η = {self.eta*100:.1f}%")
            
            # Propager le changement en amont si nécessaire
            if hasattr(self.Inlet, 'callback') and self.Inlet.callback:
                self.Inlet.callback()
        else:
            print(f"⚠️  Échec recherche débit: {result.message}")
        
    def calculate (self):
        # Marquer qu'on est en train de calculer pour éviter le callback
        self._calculating = True
        
        if self.Pdischarge_bar is not None:
            self.Pdischarge=self.Pdischarge_bar*100000

        self.Ti_degC=-273.15+PropsSI("T", "P", self.Inlet.P, "H", self.Inlet.h, self.Inlet.fluid)
        #print("Ti_degC",self.Ti_degC)
        if self.Inlet.F is not None:
            self.F_m3s =self.Inlet.F/PropsSI("D", "P", self.Inlet.P, "T", (self.Ti_degC+273.15), self.Inlet.fluid)
            self.F_m3h=self.F_m3s*3600
        #print("F_m3s",self.F_m3s)

        

        
    #     # outlet connector calculation
        self.Outlet.fluid=self.Inlet.fluid
        self.Outlet.h=self.Inlet.h
        self.Outlet.F=self.Inlet.F
        
        # Désactiver temporairement le callback pour éviter les boucles infinies
        original_callback = self.Outlet.callback
        self.Outlet.callback = None
        
        self.Outlet.P=self.Inlet.P
        
        # Réactiver le callback après l'initialisation
        self.Outlet.callback = original_callback


        #Corrélation de la courbe caractéristique de la pompe
        #pip install scikit-learn
        from sklearn.linear_model import LinearRegression  
        from sklearn.preprocessing import PolynomialFeatures 
        from sklearn.metrics import mean_squared_error, r2_score



        #----------------------------------------------------------------------------------------#
        # Step 1: training data
        if self.X_F is None:
            self.X_F = [7,50,100,150]
        if self.Y_hmt is None:
            self.Y_hmt = [12,60,80,68]
        if self.Y_eta is None:
            self.Y_eta = [0.5,0.7,0.5,0.4]
        
       
        #print(max(self.X_F))
        self.X_F = np.asarray(self.X_F)
        max_x=max(self.X_F)
        self.Y_hmt = np.asarray(self.Y_hmt)
        self.max_Y_hmt=max(self.Y_hmt)
        self.Y_eta = np.asarray(self.Y_eta)
        max_Y_eta=max(self.Y_eta)


        self.X_F = self.X_F[:,np.newaxis]
        self.Y_hmt = self.Y_hmt[:,np.newaxis]
        self.Y_eta = self.Y_eta[:,np.newaxis]


        #----------------------------------------------------------------------------------------#
        # Step 2: data preparation

        self.nb_degree = len(self.X_F)-1

        self.polynomial_features = PolynomialFeatures(degree = self.nb_degree)

        X_TRANSF = self.polynomial_features.fit_transform(self.X_F)
       

        #----------------------------------------------------------------------------------------#
        # Step 3: define and train a model

        self.model_hmt = LinearRegression()
        self.model_eta = LinearRegression()

        #self.model_hmt.fit(X_TRANSF, self.Y_hmt)
        self.model_hmt.fit(X_TRANSF, self.Y_hmt)
        self.model_eta.fit(X_TRANSF, self.Y_eta)

        #----------------------------------------------------------------------------------------#
        # Step 4: calculate bias and variance

        self.Y_hmt_NEW = self.model_hmt.predict(X_TRANSF)
        self.Y_eta_NEW = self.model_eta.predict(X_TRANSF)

        self.rmse_hmt = np.sqrt(mean_squared_error(self.Y_hmt,self.Y_hmt_NEW))
        self.r2_hmt = r2_score(self.Y_hmt,self.Y_hmt_NEW)
        #print('RMSE: ', self.rmse_hmt)
        #print('R2: ', self.r2_hmt)

        rmse_eta = np.sqrt(mean_squared_error(self.Y_eta,self.Y_eta_NEW))
        r2_eta = r2_score(self.Y_eta,self.Y_eta_NEW)
        #print('RMSE: ', rmse_eta)
        #print('R2: ', r2_eta)

        #----------------------------------------------------------------------------------------#
        # Step 5: prediction

        self.x_new_min = 0.0
        # Étendre la plage pour inclure les points de fonctionnement potentiels
        base_max = 1.05 * max_x
        if self.F_m3h is not None:
            # S'assurer que le point de fonctionnement est dans la plage
            self.x_new_max = max(base_max, 1.2 * self.F_m3h)
        else:
            self.x_new_max = base_max

        self.X_NEW = np.linspace(self.x_new_min, self.x_new_max, 100)
        self.X_NEW = self.X_NEW[:,np.newaxis]
        #print(self.X_NEW)

        X_NEW_TRANSF = self.polynomial_features.fit_transform(self.X_NEW)
   

        self.Y_hmt_NEW = self.model_hmt.predict(X_NEW_TRANSF)
        self.Y_eta_NEW = self.model_eta.predict(X_NEW_TRANSF)

        #calculer hmt et delta_p pour le point de fonctionnement self.m3/h
        if self.F_m3h is not None and self.Pdischarge is None:
            self.calculate_hmt()

        if self.Pdischarge is not None:
            self.calculate_flow_rate()
        
        if self.F_m3h is not None:
            self.calculate_eta()

        try:
            self.Q_pump=self.F_m3s*(self.Pdischarge-self.Inlet.P)/self.eta
        except:
            self.Q_pump=self.F_m3s*(self.delta_p)/self.eta

        # Désactiver temporairement le callback pour mettre à jour Outlet.P
        original_callback = self.Outlet.callback
        self.Outlet.callback = None
        
        # Mettre à jour la pression de sortie
        if self.Pdischarge is not None:
            self.Outlet.P = self.Pdischarge
        else:
            self.Outlet.P = self.Inlet.P + self.delta_p
        
        # Réactiver le callback
        self.Outlet.callback = original_callback
        
        # Fin du calcul initial, autoriser les callbacks
        if hasattr(self, '_calculating'):
            delattr(self, '_calculating')

        #-----------------------------------------------------------------------------------------#
        # sortir les résultats sous forme de dataframe avec le débit volumique et la hauteur manométrique du point de fonctionnement

        self.df = pd.DataFrame({'Pump': [self.Timestamp,self.Inlet.fluid,self.Inlet.F,self.F_m3h,self.hmt,self.delta_p,self.Q_pump/1000,self.eta,], },
                      index = ['Timestamp','pump_fluid','pump_F_kgs','pump_F_m3h','hmt(m)','delta_p (Pa)','Qpump(KW)','self.eta' ])


    def calculate_eta(self):
        """
        Calcule le rendement (eta) de la pompe en fonction du débit volumique (F_m3h)
        en utilisant la corrélation.

        Returns:
            float: Rendement (eta) de la pompe.
        """
        if self.model_eta is None:
            raise ValueError("Le modèle de rendement (eta) doit être entraîné avant de l'utiliser.")

        if self.F_m3h is None:
            raise ValueError("Le débit volumique (F_m3h) doit être calculé avant de prédire le rendement.")

        # Transformer le débit volumique pour le modèle
        F_m3h_array = np.array([[self.F_m3h]])  # Assurez-vous que F_m3h est un tableau 2D
        F_transformed = self.polynomial_features.transform(F_m3h_array)

        # Prédire le rendement
        self.eta = self.model_eta.predict(F_transformed)[0][0]
        return self.eta

    def calculate_flow_rate(self):
        """
        Calcule le débit volumique (F_m3h) en fonction des pressions d'entrée et de sortie,
        et de la hauteur manométrique calculée à partir de la corrélation.

        Returns:
            float: Débit volumique (F_m3h) en m³/h.
        """
        if self.Inlet.P is None or self.Pdischarge is None:
            raise ValueError("Les pressions d'entrée et de sortie doivent être définies.")

        if self.model_hmt is None:
            raise ValueError("Le modèle de hauteur manométrique (Hmt) doit être entraîné avant de l'utiliser.")

        # Calculer la hauteur manométrique (Hmt) à partir des pressions
        rho = PropsSI("D", "P", self.Inlet.P, "T", self.Ti_degC + 273.15, self.Inlet.fluid)
        g = 9.81  # Accélération gravitationnelle en m/s²
        self.delta_p = self.Pdischarge - self.Inlet.P
        self.hmt = self.delta_p / (rho * g)
        # print("Hauteur manométrique calculée (self.hmt):", self.hmt)

        # Fonction d'erreur pour minimisation
        def error_function(F_m3h):
            """
            Fonction d'erreur pour la minimisation.
            Compare la hauteur manométrique prédite avec la hauteur calculée.
            """
            F_m3h_array = np.array(F_m3h).reshape(-1, 1)  # Convertir en tableau 2D
            F_transformed = self.polynomial_features.transform(F_m3h_array)
            hmt_predicted = self.model_hmt.predict(F_transformed)[0][0]
            return abs(hmt_predicted - self.hmt)

        # Estimation initiale et bornes
        initial_guess = self.F_m3h if self.F_m3h is not None else self.X_F[0][0]  # Utiliser une estimation existante ou le premier point
        bounds = [(0.1, 1.5 * max(self.X_F))]  # Débit volumique entre 0.1 et 1.5 fois le maximum des données

        # Recherche numérique pour minimiser l'erreur
        result = minimize(
            error_function,
            x0=initial_guess,
            bounds=bounds,
            method='L-BFGS-B',  # Méthode robuste pour les problèmes avec bornes
            options={'ftol': 1e-6, 'disp': False}  # Tolérance plus stricte pour une meilleure précision
        )

        if result.success:
            self.F_m3h = result.x[0]
            # print("Débit volumique calculé (self.F_m3h):", self.F_m3h)
        else:
            raise ValueError(f"La recherche numérique pour le débit volumique a échoué : {result.message}")


    def calculate_hmt(self):
        """
        Calcule la hauteur manométrique (Hmt) à partir de la corrélation pour X_F = self.F_m3h.

        Returns:
            float: Hauteur manométrique prédite (Hmt) en mètres.
        """
        if self.model_hmt is None:
            raise ValueError("Le modèle de hauteur manométrique (Hmt) doit être entraîné avant de l'utiliser.")

        if self.F_m3h is None:
            raise ValueError("Le débit volumique (F_m3h) doit être calculé avant de prédire Hmt.")

        # Transformer le débit volumique pour le modèle
        F_m3h_array = np.array([[self.F_m3h]])
        F_transformed = self.polynomial_features.transform(F_m3h_array)

        # Prédire la hauteur manométrique
        self.hmt = self.model_hmt.predict(F_transformed)[0][0]
        
            # Obtenir la densité du fluide à l'entrée
        rho = PropsSI("D", "P", self.Inlet.P, "T", self.Ti_degC + 273.15, self.Inlet.fluid)

        # Accélération gravitationnelle
        g = 9.81  # m/s²

        # Calcul de la différence de pression
        self.delta_p = rho * g * self.hmt

    

        #----------------------------------------------------------------------------------------#
        # Step 6: Plotting

        
    def plot_pump_curve(self, figsize=(14, 10)):
        """
        Trace la courbe caractéristique de la pompe avec deux graphiques séparés :
        - Graphique supérieur : Hauteur manométrique (Hmt) et pression (ΔP)
        - Graphique inférieur : Rendement (eta)
        Affiche les points de construction, le point de fonctionnement avec correspondance entre les deux graphiques.
        """
        # Calculer la densité du fluide pour convertir Hmt en bar
        rho = PropsSI("D", "P", self.Inlet.P, "T", self.Ti_degC + 273.15, self.Inlet.fluid)
        g = 9.81  # Accélération gravitationnelle en m/s²
        
        # Convertir les données en pression (bar)
        Y_pressure_NEW = self.Y_hmt_NEW * rho * g / 100000  # Conversion Hmt → bar
        Y_pressure_points = self.Y_hmt.flatten() * rho * g / 100000
        
        # Créer une figure avec deux sous-graphiques
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
        fig.suptitle('COURBE CARACTÉRISTIQUE DE LA POMPE', fontsize=16, fontweight='bold')
        
        # ========================================================================
        # GRAPHIQUE 1 : HAUTEUR MANOMÉTRIQUE ET PRESSION
        # ========================================================================
        
        # Courbe HMT
        line_hmt = ax1.plot(self.X_NEW, self.Y_hmt_NEW, color='#FF6B35', linewidth=3, 
                            label='Courbe HMT (corrélation)', zorder=5)
        ax1.set_ylabel('Hauteur Manométrique (m)', color='#FF6B35', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor='#FF6B35', labelsize=10)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Axe secondaire pour la pression
        ax1_pressure = ax1.twinx()
        ax1_pressure.plot(self.X_NEW, Y_pressure_NEW, color='#004E89', linewidth=3, 
                         linestyle='--', label='Courbe ΔP (bar)', alpha=0.7, zorder=5)
        ax1_pressure.set_ylabel('Pression ΔP (bar)', color='#004E89', fontsize=12, fontweight='bold')
        ax1_pressure.tick_params(axis='y', labelcolor='#004E89', labelsize=10)
        
        # Points de construction caractéristiques (HMT)
        ax1.scatter(self.X_F.flatten(), self.Y_hmt.flatten(), color='#FF6B35', 
                   s=150, marker='s', edgecolors='black', linewidth=2, 
                   label='Points construction HMT', zorder=10)
        
        # Annotations pour les points de construction (HMT)
        for i, (x, y) in enumerate(zip(self.X_F.flatten(), self.Y_hmt.flatten())):
            ax1.annotate(f'P{i+1}\n{x:.1f} m³/h\n{y:.1f} m', 
                        xy=(x, y), xytext=(10, 10), textcoords='offset points',
                        fontsize=8, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FF6B35', alpha=0.3),
                        arrowprops=dict(arrowstyle='->', color='#FF6B35', lw=1.5))
        
        # Point de fonctionnement (HMT)
        if self.F_m3h is not None and self.hmt is not None:
            pressure_operating = self.hmt * rho * g / 100000
            
            # Point sur HMT
            ax1.scatter([self.F_m3h], [self.hmt], color='red', s=300, marker='*', 
                       edgecolors='darkred', linewidth=2, label='Point fonctionnement', zorder=15)
            
            # Point sur pression
            ax1_pressure.scatter([self.F_m3h], [pressure_operating], color='red', 
                                s=200, marker='*', edgecolors='darkred', linewidth=2, zorder=15)
            
            # Lignes de correspondance
            ax1.axvline(self.F_m3h, color='red', linestyle=':', linewidth=2, alpha=0.5, zorder=3)
            ax1.axhline(self.hmt, color='red', linestyle=':', linewidth=2, alpha=0.5, zorder=3)
            
            # Annotation du point de fonctionnement
            ax1.annotate(f'FONCTIONNEMENT\nQ = {self.F_m3h:.2f} m³/h\nHMT = {self.hmt:.2f} m\nΔP = {pressure_operating:.3f} bar',
                        xy=(self.F_m3h, self.hmt), xytext=(30, -30), textcoords='offset points',
                        fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.8', facecolor='red', alpha=0.2, edgecolor='darkred', linewidth=2),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # Limites et légendes
        ax1.set_ylim(0, 1.1 * self.max_Y_hmt)
        ax1_pressure.set_ylim(0, 1.1 * max(Y_pressure_points))
        
        # Légendes combinées
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_pressure.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9, framealpha=0.9)
        
        # ========================================================================
        # GRAPHIQUE 2 : RENDEMENT
        # ========================================================================
        
        # Courbe rendement
        ax2.plot(self.X_NEW, self.Y_eta_NEW * 100, color='#1B9C85', linewidth=3, 
                label='Courbe rendement (corrélation)', zorder=5)
        ax2.set_xlabel('Débit volumique (m³/h)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Rendement η (%)', color='#1B9C85', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='#1B9C85', labelsize=10)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        # Points de construction caractéristiques (rendement)
        ax2.scatter(self.X_F.flatten(), self.Y_eta.flatten() * 100, color='#1B9C85', 
                   s=150, marker='s', edgecolors='black', linewidth=2,
                   label='Points construction η', zorder=10)
        
        # Annotations pour les points de construction (rendement)
        for i, (x, y) in enumerate(zip(self.X_F.flatten(), self.Y_eta.flatten())):
            ax2.annotate(f'P{i+1}\n{x:.1f} m³/h\n{y*100:.1f}%', 
                        xy=(x, y*100), xytext=(10, -15), textcoords='offset points',
                        fontsize=8, bbox=dict(boxstyle='round,pad=0.5', facecolor='#1B9C85', alpha=0.3),
                        arrowprops=dict(arrowstyle='->', color='#1B9C85', lw=1.5))
        
        # Point de fonctionnement (rendement)
        if self.F_m3h is not None and self.eta is not None:
            ax2.scatter([self.F_m3h], [self.eta * 100], color='red', s=300, marker='*',
                       edgecolors='darkred', linewidth=2, label='Point fonctionnement', zorder=15)
            
            # Lignes de correspondance
            ax2.axvline(self.F_m3h, color='red', linestyle=':', linewidth=2, alpha=0.5, zorder=3)
            ax2.axhline(self.eta * 100, color='red', linestyle=':', linewidth=2, alpha=0.5, zorder=3)
            
            # Annotation du point de fonctionnement
            ax2.annotate(f'FONCTIONNEMENT\nQ = {self.F_m3h:.2f} m³/h\nη = {self.eta*100:.2f}%',
                        xy=(self.F_m3h, self.eta * 100), xytext=(30, 15), textcoords='offset points',
                        fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.8', facecolor='red', alpha=0.2, edgecolor='darkred', linewidth=2),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # Limites et légende - S'assurer que le point de fonctionnement est visible
        x_max_display = self.x_new_max
        if self.F_m3h is not None:
            x_max_display = max(x_max_display, self.F_m3h * 1.1)
        
        ax2.set_xlim(self.x_new_min, x_max_display)
        ax2.set_ylim(0, 105)
        ax2.legend(loc='upper right', fontsize=9, framealpha=0.9)
        
        # ========================================================================
        # INFORMATIONS SUPPLÉMENTAIRES
        # ========================================================================
        
        # Ajouter un encadré d'informations
        info_text = f'Corrélation polynomiale : degré {self.nb_degree}\n'
        info_text += f'RMSE (HMT) : {self.rmse_hmt:.4f} m\n'
        info_text += f'R² (HMT) : {self.r2_hmt:.4f}\n'
        info_text += f'Fluide : {self.Inlet.fluid} @ {self.Ti_degC:.1f}°C'
        
        fig.text(0.02, 0.02, info_text, fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                verticalalignment='bottom', horizontalalignment='left')
        
        # Ajuster l'espacement
        plt.tight_layout(rect=[0, 0.05, 1, 0.97])
        plt.show() 