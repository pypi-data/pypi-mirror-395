"""
Module GenericAHU - Centrale de Traitement d'Air Générique Paramétrable

Ce module implémente une classe de CTA (Centrale de Traitement d'Air) générique 
qui permet de simuler différentes configurations d'unités de traitement d'air 
à partir d'un fichier Excel de configuration.

La classe supporte deux modes principaux :
1. Mode Recyclage (Recycling) : Mélange d'air neuf et d'air recyclé
2. Mode Récupération (Recovery) : Récupération de chaleur sur air extrait

Auteur: Zoheir HADID
Date: 2024
"""

import pandas as pd
import warnings
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from AHU.air_humide import air_humide
from AHU.FreshAir.FreshAir import Object as FreshAir
from AHU.FreshAir.AirMix import Object as AirMix
from AHU.Coil.HeatingCoil import Object as HeatingCoil
from AHU.Coil.CoolingCoil_Expert import Object as CoolingCoil_Expert
from AHU.Humidification.Humidifier import Object as Humidifier
from AHU.Connect import Air_connect
from AHU.HeatRecovery.Heat_plate_exchanger import Object as Heat_plate_exchanger

# Tentative d'import de la roue thermique (peut ne pas exister)
try:
    from AHU.HeatRecovery.Thermal_wheel_exchanger import Object as Thermal_wheel_exchanger
except ImportError:
    Thermal_wheel_exchanger = None
    warnings.warn("Thermal_wheel_exchanger non disponible, seul Heat_plate_exchanger sera utilisé")

warnings.filterwarnings("ignore", category=RuntimeWarning)


class GenericAHU:
    """
    Classe générique de Centrale de Traitement d'Air (CTA) paramétrable.
    
    Cette classe permet de configurer et simuler des systèmes de traitement d'air
    complexes avec différents composants (batteries, humidificateurs, échangeurs, etc.)
    à partir d'un fichier de configuration Excel.
    
    Attributes:
        config_file (str): Chemin vers le fichier Excel de configuration
        mode (str): Mode de fonctionnement ('recycling' ou 'recovery')
        config (dict): Configuration des composants actifs
        data (pd.DataFrame): Données temporelles d'entrée
        results (pd.DataFrame): Résultats de la simulation
        component_logs (dict): Logs détaillés par composant
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialise la CTA générique.
        
        Args:
            config_file: Chemin vers le fichier Excel de configuration (optionnel)
        """
        self.config_file = config_file
        self.mode = None
        self.config = {}
        self.data = None
        self.config_data = None
        self.results = None
        self.component_logs = {}
        
    def load_excel_config(self, file_path: str, sheet_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Charge les données de configuration et les données temporelles depuis Excel.
        
        Args:
            file_path: Chemin vers le fichier Excel
            sheet_name: Nom de la feuille à charger
            
        Returns:
            Tuple contenant (config_data, time_series_data)
        """
        # Lecture de la configuration (2 premières lignes après l'en-tête)
        config_data = pd.read_excel(file_path, sheet_name=sheet_name, header=None, 
                                    skiprows=6, nrows=2)
        
        # Lecture des données temporelles
        data = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=9)
        
        # Nettoyage des noms de colonnes
        data.columns = (data.columns.str.strip()
                       .str.replace('\n', ' ', regex=True)
                       .str.replace('\r', '')
                       .str.replace(' +', ' ', regex=True))
        
        print(f"✅ Données chargées depuis : {sheet_name}")
        print(f"📋 Colonnes disponibles : {list(data.columns)}")
        
        self.config_data = config_data
        self.data = data
        
        return config_data, data
    
    def parse_config_recycling(self, config_data: pd.DataFrame) -> Dict:
        """
        Parse la configuration pour le mode recyclage.
        
        Args:
            config_data: DataFrame contenant la configuration
            
        Returns:
            Dictionnaire de configuration
        """
        config = {
            "recycling": False,
            "pre_heating_coil": False,
            "heating_coil": False,
            "cooling_coil": False,
            "humidifier": False,
            "humidifier_type": "adiabatique",
            "post_heating_coil": False
        }
        
        for j in range(config_data.shape[1]):
            component = str(config_data.iat[0, j]).strip().lower()
            value = str(config_data.iat[1, j]).strip().lower()
            
            if component == 'recycling':
                config["recycling"] = value == "yes"
            elif component == 'defrost coil':
                config["pre_heating_coil"] = value == "yes"
            elif component == 'heating coil':
                config["heating_coil"] = value == "yes"
            elif component == 'cooling coil':
                config["cooling_coil"] = value == "yes"
            elif component == 'humidifier':
                if value == "yes spray":
                    config["humidifier"] = True
                    config["humidifier_type"] = "adiabatique"
                elif value == "yes steam":
                    config["humidifier"] = True
                    config["humidifier_type"] = "vapeur"
                else:
                    config["humidifier"] = False
                    config["humidifier_type"] = None
            elif component == 'post heating coil':
                config["post_heating_coil"] = value == "yes"
        
        self.config = config
        return config
    
    def parse_config_recovery(self, config_data: pd.DataFrame) -> Dict:
        """
        Parse la configuration pour le mode récupération.
        
        Args:
            config_data: DataFrame contenant la configuration
            
        Returns:
            Dictionnaire de configuration
        """
        config = {
            "exchange_type": "none",
            "pre_heating_coil": False,
            "heating_coil": False,
            "cooling_coil": False,
            "humidifier": False,
            "humidifier_type": "adiabatique",
            "post_heating_coil": False,
            "heat_exchanger": False
        }
        
        for j in range(config_data.shape[1]):
            component = str(config_data.iat[0, j]).strip().lower()
            value = str(config_data.iat[1, j]).strip().lower()
            
            if component == 'heat exchanger':
                config["heat_exchanger"] = value in ["yes heat plate exchanger", 
                                                     "yes energy wheel exchanger"]
                if value == "yes heat plate exchanger":
                    config["exchange_type"] = "heat plate exchanger"
                elif value == "yes energy wheel exchanger":
                    config["exchange_type"] = "energy wheel exchanger"
            elif component == 'defrost coil':
                config["pre_heating_coil"] = value == "yes"
            elif component == 'heating coil':
                config["heating_coil"] = value == "yes"
            elif component == 'cooling coil':
                config["cooling_coil"] = value == "yes"
            elif component == 'humidifier':
                if value == "yes spray":
                    config["humidifier"] = True
                    config["humidifier_type"] = "adiabatique"
                elif value == "yes steam":
                    config["humidifier"] = True
                    config["humidifier_type"] = "vapeur"
                else:
                    config["humidifier"] = False
                    config["humidifier_type"] = None
            elif component == 'post heating coil':
                config["post_heating_coil"] = value == "yes"
        
        self.config = config
        return config
    
    def log_raw_air_point(self, key: str, air_obj, decimals: int = 2):
        """
        Enregistre les données brutes d'un point d'air.
        
        Args:
            key: Clé d'identification du composant
            air_obj: Objet air à logger (FreshAir)
            decimals: Nombre de décimales pour l'arrondi
        """
        if key not in self.component_logs:
            self.component_logs[key] = []
        
        self.component_logs[key].append({
            "T[°C]": round(air_obj.T, decimals),
            "RH[%]": round(air_obj.RH, decimals),
            "F_dry[kgas/s]": round(air_obj.F_dry, decimals),
            "h[kJ/kgda]": round(air_obj.h, decimals),
            "w[gH2O/kgda]": round(air_obj.w, decimals),
            "F_m3h[m3/h]": round(air_obj.F_dry / air_humide.Air_rho_hum(
                T_db=air_obj.T, RH=air_obj.RH) * 3600, decimals)
        })
    
    def log_air_point(self, component_name: str, obj, Q_th: Optional[float] = None, 
                     F_water: Optional[float] = None, decimals: int = 2):
        """
        Enregistre les données d'air en entrée et sortie d'un composant.
        
        Args:
            component_name: Nom du composant
            obj: Objet composant à logger
            Q_th: Puissance thermique (optionnel)
            F_water: Débit d'eau (optionnel)
            decimals: Nombre de décimales pour l'arrondi
        """
        if component_name not in self.component_logs:
            self.component_logs[component_name] = []
        
        def extract_air_data(air_obj, label):
            """Extrait les données d'un objet air."""
            return {
                f"{label}_T[°C]": round(air_obj.T, decimals),
                f"{label}_RH[%]": round(air_obj.RH, decimals),
                f"{label}_h[kJ/kgas]": round(air_obj.h, decimals),
                f"{label}_w[gH20/kgda]": round(air_obj.w, decimals),
                f"{label}_F[kg/s]": round(getattr(air_obj, "F", 0), decimals) 
                    if getattr(air_obj, "F", None) is not None else None,
                f"{label}_F_dry[kgas/s]": round(air_obj.F_dry, decimals),
                f"{label}F_m3h[m3/h]": round(air_obj.F_dry / air_humide.Air_rho_hum(
                    T_db=air_obj.T, RH=air_obj.RH) * 3600, decimals),
                f"{label}_P[Pa]": round(getattr(air_obj, "P", 0), decimals) 
                    if getattr(air_obj, "P", None) is not None else None,
                f"{label}_Pv_sat[Pa]": round(getattr(air_obj, "Pv_sat", 0), decimals) 
                    if getattr(air_obj, "Pv_sat", None) is not None else None
            }
        
        entry = {}
        
        # Cas échangeur : 2 entrées / 2 sorties
        if (hasattr(obj, "Inlet1") and hasattr(obj, "Outlet1") and 
            hasattr(obj, "Inlet2") and hasattr(obj, "Outlet2")):
            entry.update(extract_air_data(obj.Inlet1, "Inlet1"))
            entry.update(extract_air_data(obj.Outlet1, "Outlet1"))
            entry.update(extract_air_data(obj.Inlet2, "Inlet2"))
            entry.update(extract_air_data(obj.Outlet2, "Outlet2"))
            
            # Métriques spécifiques échangeurs
            if hasattr(obj, "heat_transfer1"):
                entry["Heat_recovery[kW]"] = round(obj.heat_transfer1, decimals)
            if hasattr(obj, "sensible_heat_transfer1"):
                entry["Sensible_heat1[kW]"] = round(obj.sensible_heat_transfer1, decimals)
            if hasattr(obj, "sensible_heat_transfer2"):
                entry["Sensible_heat2[kW]"] = round(obj.sensible_heat_transfer2, decimals)
            if hasattr(obj, "delta_mw1"):
                entry["Δmw1[gH2O/kgas]"] = round(obj.delta_mw1, decimals)
            if hasattr(obj, "delta_mw2"):
                entry["Δmw2[gH2O/kgas]"] = round(obj.delta_mw2, decimals)
            if hasattr(obj, "T_efficiency"):
                entry["T_efficiency[%]"] = round(obj.T_efficiency, decimals)
            if hasattr(obj, "h_efficiency"):
                entry["h_efficiency[%]"] = round(obj.h_efficiency, decimals)
        
        # Cas standard : un seul point de sortie
        elif hasattr(obj, "Outlet"):
            entry.update(extract_air_data(obj.Outlet, "Outlet"))
            if Q_th is not None:
                entry["Q_th[kW]"] = round(Q_th, decimals)
            if F_water is not None:
                entry["F_water[kg/h]"] = round(F_water, decimals)
        
        else:
            print(f"⚠️ Composant {component_name} non reconnu pour log_air_point.")
        
        self.component_logs[component_name].append(entry)
    
    def simulate_recycling(self, progress_callback=None) -> pd.DataFrame:
        """
        Simule le mode recyclage (mélange air neuf + air recyclé).
        
        Args:
            progress_callback: Fonction de callback pour suivre la progression
            
        Returns:
            DataFrame contenant tous les résultats de simulation
        """
        if self.data is None:
            raise ValueError("Aucune donnée chargée. Utilisez load_excel_config() d'abord.")
        
        print("▶️ Mode RECYCLAGE activé")
        
        # Initialisation des logs
        self.component_logs = {
            "FA": [], "RA": [], "AMX": [], "MXA": [],
            "PREHC": [], "HC": [], "CC": [], "HMD": [], "POSTHC": []
        }
        
        total = len(self.data)
        
        for index, row in self.data.iterrows():
            try:
                total_flow = row['Supply Air flow [m3/h]']
                recyc_pct = row['Mix Recycled Air [%]']
                T_consigne = row['Supply Air Set Point [T°C]']
                w_target = air_humide.Air_w(T_db=T_consigne, 
                                            RH=row['Supply Air Set Point [HR %]'])
                
                # Air neuf
                FA = FreshAir()
                FA.T = row['Fresh Air [T°C]']
                FA.RH = row['Fresh Air [HR %]']
                FA.F_m3h = total_flow * (1 - recyc_pct / 100)
                FA.calculate()
                self.log_raw_air_point("FA", FA)
                
                # Air recyclé si activé
                if self.config["recycling"] and recyc_pct > 0:
                    RA = FreshAir()
                    RA.T = row['Recycled Air [T°C]']
                    RA.RH = row['Recycled Air [HR %]']
                    RA.F_m3h = total_flow * (recyc_pct / 100)
                    RA.calculate()
                    self.log_raw_air_point("RA", RA)
                    
                    # Mélange
                    AMX = AirMix()
                    Air_connect(AMX.Inlet1, FA.Outlet)
                    Air_connect(AMX.Inlet2, RA.Outlet)
                    AMX.calculate()
                    self.log_air_point("AMX", AMX)
                    
                    # Air mélangé
                    MXA = FreshAir()
                    Air_connect(MXA.Inlet, AMX.Outlet)
                    MXA.T = air_humide.Air_T_db(h=AMX.Outlet.h, w=AMX.Outlet.w)
                    MXA.RH = air_humide.Air_RH(h=AMX.Outlet.h, w=AMX.Outlet.w)
                    MXA.F_m3h = total_flow
                    MXA.calculate()
                else:
                    MXA = FreshAir()
                    MXA.T = FA.T
                    MXA.RH = FA.RH
                    MXA.F_m3h = total_flow
                    MXA.calculate()
                
                self.log_air_point("MXA", MXA)
                current_air = MXA
                
                # Batterie de préchauffage (dégivrage)
                if self.config["pre_heating_coil"]:
                    PREHC = HeatingCoil()
                    PREHC.To_target = row.get('Defrost Coil Set Point [T°C]', None)
                    Air_connect(PREHC.Inlet, current_air.Outlet)
                    PREHC.calculate()
                    self.log_air_point("PREHC", PREHC, Q_th=PREHC.Q_th)
                    current_air = PREHC
                
                # Batterie de chauffage
                if self.config["heating_coil"]:
                    HC = HeatingCoil()
                    HC.To_target = T_consigne
                    Air_connect(HC.Inlet, current_air.Outlet)
                    HC.calculate()
                    self.log_air_point("HC", HC, Q_th=HC.Q_th)
                    current_air = HC
                
                # Batterie de refroidissement
                if self.config["cooling_coil"]:
                    CC = CoolingCoil_Expert()
                    CC.T_target = T_consigne
                    CC.w_target = w_target
                    Air_connect(CC.Inlet, current_air.Outlet)
                    CC.calculate()
                    self.log_air_point("CC", CC, Q_th=CC.Q_th)
                    current_air = CC
                
                # Humidificateur
                if self.config["humidifier"]:
                    HMD = Humidifier()
                    HMD.wo_target = w_target
                    HMD.HumidType = self.config["humidifier_type"]
                    Air_connect(HMD.Inlet, current_air.Outlet)
                    HMD.calculate()
                    self.log_air_point("HMD", HMD, Q_th=HMD.Q_th, F_water=HMD.F_water)
                    current_air = HMD
                
                # Batterie de post-chauffage
                if self.config["post_heating_coil"]:
                    POSTHC = HeatingCoil()
                    POSTHC.To_target = T_consigne
                    Air_connect(POSTHC.Inlet, current_air.Outlet)
                    POSTHC.calculate()
                    self.log_air_point("POSTHC", POSTHC, Q_th=POSTHC.Q_th)
                    current_air = POSTHC
                
                # Callback de progression
                if progress_callback:
                    progress_callback(index + 1, total)
                    
            except Exception as e:
                print(f"⚠️ Erreur ligne {index + 1} : {e}")
                continue
        
        # Compilation des résultats
        self.results = self._compile_results()
        print("✅ Simulation recyclage terminée")
        return self.results
    
    def simulate_recovery(self, progress_callback=None) -> pd.DataFrame:
        """
        Simule le mode récupération (échangeur sur air extrait).
        
        Args:
            progress_callback: Fonction de callback pour suivre la progression
            
        Returns:
            DataFrame contenant tous les résultats de simulation
        """
        if self.data is None:
            raise ValueError("Aucune donnée chargée. Utilisez load_excel_config() d'abord.")
        
        print("▶️ Mode RÉCUPÉRATION activé")
        
        # Initialisation des logs
        self.component_logs = {
            "FA": [], "EA": [], "EXC": [],
            "PREHC": [], "HC": [], "CC": [], "HMD": [], "POSTHC": []
        }
        
        total = len(self.data)
        
        for index, row in self.data.iterrows():
            try:
                # Air neuf
                FA = FreshAir()
                FA.T = row['Fresh Air [T°C]']
                FA.RH = row['Fresh Air [HR %]']
                FA.F_m3h = row['Fresh Air [m3/h]']
                FA.calculate()
                self.log_raw_air_point("FA", FA)
                
                # Air extrait
                EA = FreshAir()
                EA.T = row['Extracted Air [T°C]']
                EA.RH = row['Extracted Air [HR %]']
                EA.F_m3h = row['Extracted Air [m3/h]']
                EA.calculate()
                self.log_raw_air_point("EA", EA)
                
                T_set = row['Supply Air Set Point [T°C]']
                RH_set = row['Supply Air Set Point [HR %]']
                w_set = air_humide.Air_w(T_db=T_set, RH=RH_set)
                
                # Échangeur de récupération
                exchanger = None
                if self.config["heat_exchanger"]:
                    if self.config["exchange_type"] == "heat plate exchanger":
                        exchanger = Heat_plate_exchanger()
                    elif self.config["exchange_type"] == "energy wheel exchanger":
                        if Thermal_wheel_exchanger is not None:
                            exchanger = Thermal_wheel_exchanger()
                        else:
                            print("⚠️ Roue thermique non disponible, utilisation échangeur à plaques")
                            exchanger = Heat_plate_exchanger()
                
                if exchanger:
                    exchanger.T_efficiency = row.get('Heat exchanger efficiency [%]', 70)
                    exchanger.T_target = T_set
                    Air_connect(exchanger.Inlet1, FA.Outlet)
                    Air_connect(exchanger.Inlet2, EA.Outlet)
                    exchanger.Outlet1.F = exchanger.Inlet1.F
                    exchanger.Outlet2.F = exchanger.Inlet2.F
                    exchanger.calculate()
                    self.log_air_point("EXC", exchanger)
                    current_air = exchanger.Outlet1
                else:
                    current_air = FA.Outlet
                
                # Batterie de préchauffage (dégivrage)
                if self.config["pre_heating_coil"]:
                    PREHC = HeatingCoil()
                    PREHC.To_target = row.get('Defrost Coil Set Point [T°C]', None)
                    Air_connect(PREHC.Inlet, current_air)
                    PREHC.calculate()
                    self.log_air_point("PREHC", PREHC, Q_th=PREHC.Q_th)
                    current_air = PREHC.Outlet
                
                # Batterie de chauffage
                if self.config["heating_coil"]:
                    HC = HeatingCoil()
                    HC.To_target = T_set
                    Air_connect(HC.Inlet, current_air)
                    HC.calculate()
                    self.log_air_point("HC", HC, Q_th=HC.Q_th)
                    current_air = HC.Outlet
                
                # Batterie de refroidissement
                if self.config["cooling_coil"]:
                    CC = CoolingCoil_Expert()
                    CC.T_target = T_set
                    CC.w_target = w_set
                    Air_connect(CC.Inlet, current_air)
                    CC.calculate()
                    self.log_air_point("CC", CC, Q_th=CC.Q_th)
                    current_air = CC.Outlet
                
                # Humidificateur
                if self.config["humidifier"]:
                    HMD = Humidifier()
                    HMD.wo_target = w_set
                    HMD.HumidType = self.config["humidifier_type"]
                    Air_connect(HMD.Inlet, current_air)
                    HMD.calculate()
                    self.log_air_point("HMD", HMD, Q_th=HMD.Q_th, F_water=HMD.F_water)
                    current_air = HMD.Outlet
                
                # Batterie de post-chauffage
                if self.config["post_heating_coil"]:
                    POSTHC = HeatingCoil()
                    POSTHC.To_target = T_set
                    Air_connect(POSTHC.Inlet, current_air)
                    POSTHC.calculate()
                    self.log_air_point("POSTHC", POSTHC, Q_th=POSTHC.Q_th)
                    current_air = POSTHC.Outlet
                
                # Callback de progression
                if progress_callback:
                    progress_callback(index + 1, total)
                    
            except Exception as e:
                print(f"⚠️ Erreur ligne {index + 1} : {e}")
                continue
        
        # Compilation des résultats
        self.results = self._compile_results()
        print("✅ Simulation récupération terminée")
        return self.results
    
    def _compile_results(self) -> pd.DataFrame:
        """
        Compile tous les logs des composants en un DataFrame unique.
        
        Returns:
            DataFrame avec tous les résultats
        """
        merged_df = pd.DataFrame()
        
        for comp, logs in self.component_logs.items():
            if logs:  # Ne traite que les composants avec données
                df_comp = pd.DataFrame(logs)
                df_comp = df_comp.add_prefix(f"{comp}_")
                merged_df = pd.concat([merged_df, df_comp], axis=1)
        
        # Ajout du timestamp si disponible
        if self.data is not None and "Timestamp" in self.data.columns:
            merged_df.insert(0, "Timestamp", self.data["Timestamp"])
        
        return merged_df
    
    def export_to_excel(self, output_file: str, sheet_name: str = "AHU_Results"):
        """
        Exporte les résultats vers un fichier Excel.
        
        Args:
            output_file: Chemin du fichier de sortie
            sheet_name: Nom de la feuille Excel
        """
        if self.results is None:
            raise ValueError("Aucun résultat à exporter. Lancez une simulation d'abord.")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            self.results.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ Résultats exportés vers : {output_file}")
    
    def run_simulation(self, file_path: str, sheet_name: str, 
                      output_file: Optional[str] = None) -> pd.DataFrame:
        """
        Exécute une simulation complète : chargement, configuration, simulation, export.
        
        Args:
            file_path: Chemin vers le fichier Excel de configuration
            sheet_name: Nom de la feuille ('1. Air Recycling AHU Input' ou 
                       '2. Air Recovery AHU Input')
            output_file: Chemin du fichier de sortie (optionnel)
            
        Returns:
            DataFrame contenant tous les résultats
        """
        # Chargement des données
        config_data, data = self.load_excel_config(file_path, sheet_name)
        
        # Détermination du mode et parsing de la configuration
        if "Recovery" in sheet_name:
            self.mode = "recovery"
            self.parse_config_recovery(config_data)
            results = self.simulate_recovery()
        elif "Recycling" in sheet_name:
            self.mode = "recycling"
            self.parse_config_recycling(config_data)
            results = self.simulate_recycling()
        else:
            raise ValueError(f"Mode non reconnu dans le nom de feuille : {sheet_name}")
        
        # Export des résultats
        if output_file:
            self.export_to_excel(output_file)
        
        return results
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Calcule des statistiques sommaires sur les résultats.
        
        Returns:
            DataFrame avec les statistiques (min, max, moyenne, std)
        """
        if self.results is None:
            raise ValueError("Aucun résultat disponible. Lancez une simulation d'abord.")
        
        # Sélection uniquement des colonnes numériques
        numeric_cols = self.results.select_dtypes(include=['float64', 'int64']).columns
        
        stats = self.results[numeric_cols].describe()
        return stats
    
    def print_configuration(self):
        """Affiche la configuration actuelle de la CTA."""
        print("\n" + "="*60)
        print(f"CONFIGURATION CTA - Mode: {self.mode.upper() if self.mode else 'Non défini'}")
        print("="*60)
        
        if not self.config:
            print("⚠️ Aucune configuration chargée")
            return
        
        for key, value in self.config.items():
            status = "✅" if value else "❌"
            print(f"{status} {key}: {value}")
        
        print("="*60 + "\n")


# Fonctions utilitaires pour compatibilité avec le code Colab
def print_progress_bar(current: int, total: int, bar_length: int = 30):
    """
    Affiche une barre de progression dans la console.
    
    Args:
        current: Étape actuelle
        total: Nombre total d'étapes
        bar_length: Longueur de la barre
    """
    progress = int(bar_length * current / total)
    bar = "[" + "#" * progress + "-" * (bar_length - progress) + "]"
    percent = int(100 * current / total)
    print(f"\r{bar} {percent}% ({current}/{total})", end="", flush=True)
    
    if current == total:
        print()  # Nouvelle ligne à la fin


if __name__ == "__main__":
    # Exemple d'utilisation
    print("Module GenericAHU chargé avec succès !")
    print("Utilisez la classe GenericAHU pour créer et simuler vos CTA.")
