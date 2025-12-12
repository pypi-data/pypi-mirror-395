from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
from CoolProp.CoolProp import PropsSI
import pandas as pd 
import math
import matplotlib.pyplot as plt
import numpy as np

#No module named 'openpyxl'
#pip install openpyxl

class Object :
    def __init__(self):

        self.Timestamp=None
        self.Inlet=FluidPort() 
        self.Outlet=FluidPort()
        self.Outlet.callback = self.on_pressure_change  # Associer la fonction de rappel à Outlet.P
        self.df=[]
        self.delta_P=None

        self.q=None
        self.nb_tours=None
        self.dn=None

        # Données Kv organisées par DN (diamètre nominal)
        # Chaque DN contient une liste de tuples (ouverture, Kv)
        self.kv_values = {
            # STAD – PN 25 - Vanne d'équilibrage manuelle filetée (DN 10-50)
            # Source: STAD_PN25_FR_FR_low.pdf - Tableau des valeurs Kv officielles IMI TA
            "STAD-DN10": [(1, 0.091), (1.5, 0.134), (2, 0.264), (2.5, 0.461), (3, 0.799), (3.5, 1.22), (4, 1.36)],
            "STAD-DN15": [(0.5, 0.136), (1, 0.226), (1.5, 0.347), (2, 0.618), (2.5, 0.931), (3, 1.46), (3.5, 2.07), (4, 2.56)],
            "STAD-DN20": [(0.5, 0.533), (1, 0.781), (1.5, 1.22), (2, 1.95), (2.5, 2.71), (3, 3.71), (3.5, 4.51), (4, 5.39)],
            "STAD-DN25": [(0.5, 0.599), (1, 1.03), (1.5, 2.13), (2, 3.64), (2.5, 5.26), (3, 6.65), (3.5, 7.79), (4, 8.59)],
            "STAD-DN32": [(0.5, 1.19), (1, 2.09), (1.5, 3.36), (2, 5.22), (2.5, 7.77), (3, 9.82), (3.5, 11.9), (4, 14.2)],
            "STAD-DN40": [(0.5, 1.89), (1, 3.40), (1.5, 4.74), (2, 6.25), (2.5, 9.16), (3, 12.8), (3.5, 16.2), (4, 19.3)],
            "STAD-DN50": [(0.5, 2.62), (1, 4.10), (1.5, 6.76), (2, 11.4), (2.5, 15.8), (3, 21.5), (3.5, 27.0), (4, 32.3)],
            
            # STAV - Vanne d'équilibrage Venturi filetée (DN 15-50, PN 20)
            "STAV-DN15": [(0.5, 0.127), (1, 0.212), (1.5, 0.314), (2, 0.571), (2.5, 0.877), (3, 1.38), (3.5, 1.98), (4, 2.52)],
            "STAV-DN20": [(0.5, 0.511), (1, 0.757), (1.5, 1.19), (2, 1.90), (2.5, 2.80), (3, 3.87), (3.5, 4.75), (4, 5.70)],
            "STAV-DN25": [(0.5, 0.60), (1, 1.03), (1.5, 2.10), (2, 3.62), (2.5, 5.30), (3, 6.90), (3.5, 8.00), (4, 8.70)],
            "STAV-DN32": [(0.5, 1.14), (1, 1.90), (1.5, 3.10), (2, 4.66), (2.5, 7.10), (3, 9.50), (3.5, 11.8), (4, 14.2)],
            "STAV-DN40": [(0.5, 1.75), (1, 3.30), (1.5, 4.60), (2, 6.10), (2.5, 8.80), (3, 12.6), (3.5, 16.0), (4, 19.2)],
            "STAV-DN50": [(0.5, 2.56), (1, 4.20), (1.5, 7.20), (2, 11.7), (2.5, 16.2), (3, 21.5), (3.5, 26.5), (4, 33.0)],
            
            # TBV - Vanne terminale d'équilibrage manuelle (unités terminales)
            # IMI TA abaque TBV: we add LF (low-flow) and NF (normal-flow) variants.
            # TBV-LF-DN15 (Low-Flow, DN15) - positions 1..10
            "TBV-LF-DN15": [(1, 0.05), (2, 0.15), (3, 0.22), (4, 0.26), (5, 0.31), (6, 0.41), (7, 0.53), (8, 0.68), (9, 0.74), (10, 0.90)],
            # TBV-NF-DN15 (Normal-Flow, DN15) - positions 1..10
            "TBV-NF-DN15": [(1, 0.22), (2, 0.33), (3, 0.45), (4, 0.50), (5, 0.60), (6, 0.82), (7, 0.99), (8, 1.10), (9, 1.40), (10, 1.80)],
            # TBV-NF-DN20 (Normal-Flow, DN20) - positions 1..10
            "TBV-NF-DN20": [(1, 0.40), (2, 0.53), (3, 0.67), (4, 0.82), (5, 1.00), (6, 1.30), (7, 1.70), (8, 2.40), (9, 3.00), (10, 3.40)],
            # Keep generic keys as aliases to the NF variants to preserve existing code references
            "TBV-DN15": [(0.5, 0.15), (1, 0.25), (1.5, 0.38), (2, 0.65), (2.5, 0.95), (3, 1.42), (3.5, 2.05), (4, 2.60)],
            "TBV-DN20": [(0.5, 0.55), (1, 0.80), (1.5, 1.25), (2, 2.0), (2.5, 2.95), (3, 4.05), (3.5, 5.0), (4, 6.0)],
            
            # TBV-C - Vanne terminale équilibrage + contrôle (DN 10-20, avec équilibrage TA-Scope)
            "TBV-C-DN10": [(1, 0.095), (1.5, 0.145), (2, 0.275), (2.5, 0.50), (3, 0.85), (3.5, 1.30), (4, 1.52)],
            "TBV-C-DN15": [(0.5, 0.14), (1, 0.22), (1.5, 0.35), (2, 0.62), (2.5, 0.92), (3, 1.45), (3.5, 2.10), (4, 2.65)],
            "TBV-C-DN20": [(0.5, 0.53), (1, 0.78), (1.5, 1.22), (2, 1.95), (2.5, 2.90), (3, 4.0), (3.5, 4.90), (4, 5.85)],
            
            # STAF - Vanne d'équilibrage à brides fonte (DN 20-400, réseaux principaux, PN 16/25)
            # Source: STAF_STAF-SG_EN_MAIN.pdf - Tableau des valeurs Kv officielles IMI TA
            "STAF-DN20": [(0.5, 0.511), (1, 0.757), (1.5, 1.19), (2, 1.90), (2.5, 2.80), (3, 3.87), (3.5, 4.75), (4, 5.70)],
            "STAF-DN25": [(0.5, 0.60), (1, 1.03), (1.5, 2.10), (2, 3.62), (2.5, 5.30), (3, 6.90), (3.5, 8.00), (4, 8.70)],
            "STAF-DN32": [(0.5, 1.14), (1, 1.90), (1.5, 3.10), (2, 4.66), (2.5, 7.10), (3, 9.50), (3.5, 11.8), (4, 14.2)],
            "STAF-DN40": [(0.5, 1.75), (1, 3.30), (1.5, 4.60), (2, 6.10), (2.5, 8.80), (3, 12.6), (3.5, 16.0), (4, 19.2)],
            "STAF-DN50": [(0.5, 2.56), (1, 4.2), (1.5, 7.2), (2, 11.7), (2.5, 16.2), (3, 21.5), (3.5, 26.5), (4, 33)],
            "STAF-DN65": [(0.5, 1.02), (1, 2.39), (1.5, 3.77), (2, 5.18), (2.5, 6.52), (3, 8.18), (3.5, 11.6), (4, 18.6), (4.5, 29.9), (5, 39.6), (5.5, 47.9), (6, 57.5), (6.5, 66.3), (7, 74.2), (7.5, 80), (8, 85)],
            "STAF-DN80": [(0.5, 2.33), (1, 4.25), (1.5, 6.20), (2, 8.47), (2.5, 11.4), (3, 15), (3.5, 20.8), (4, 29.9), (4.5, 43.3), (5, 57.5), (5.5, 69.6), (6, 81.2), (6.5, 92.8), (7, 104), (7.5, 114), (8, 123)],
            "STAF-DN100": [(0.5, 2.5), (1, 6.0), (1.5, 9.0), (2, 11.5), (2.5, 16.0), (3, 26.0), (3.5, 44.0), (4, 63.0), (4.5, 80.0), (5, 98), (5.5, 115), (6, 132), (6.5, 145), (7, 159), (7.5, 175), (8, 190)],
            "STAF-DN125": [(0.5, 5.99), (1, 10.9), (1.5, 15.7), (2, 21.5), (2.5, 29.1), (3, 37.5), (3.5, 54.2), (4, 85.2), (4.5, 118), (5, 148), (5.5, 168), (6, 198), (6.5, 232), (7, 255), (7.5, 275), (8, 294)],
            "STAF-DN150": [(0.5, 5.39), (1, 13.3), (1.5, 22.8), (2, 41), (2.5, 65.7), (3, 92.6), (3.5, 127), (4, 176), (4.5, 214), (5, 249), (5.5, 281), (6, 307), (6.5, 332), (7, 353), (7.5, 374), (8, 400)],
            "STAF-DN200": [(2, 40), (2.5, 50), (3, 65), (3.5, 90), (4, 120), (4.5, 165), (5, 225), (5.5, 285), (6, 340), (6.5, 400), (7, 435), (7.5, 470), (8, 515), (9, 595), (10, 650), (11, 710), (12, 765)],
            "STAF-DN250": [(2, 90), (2.5, 110), (3, 140), (3.5, 195), (4, 255), (4.5, 320), (5, 385), (5.5, 445), (6, 500), (6.5, 545), (7, 590), (7.5, 660), (8, 725), (9, 820), (10, 940), (11, 1050), (12, 1185)],
            "STAF-DN300": [(3, 150), (3.5, 230), (4, 300), (4.5, 370), (5, 450), (5.5, 535), (6, 620), (6.5, 690), (7, 750), (7.5, 815), (8, 890), (9, 970), (10, 1040), (11, 1120), (12, 1200), (13, 1320), (14, 1370), (15, 1400), (16, 1450)],
            "STAF-DN350": [(3, 109), (3.5, 129), (4, 148), (4.5, 170), (5, 207), (5.5, 254), (6, 302), (6.5, 352), (7, 404), (7.5, 471), (8, 556), (9, 784), (10, 957), (11, 1100), (12, 1260), (13, 1420), (14, 1610), (15, 1760), (16, 1870), (17, 1960), (18, 2040), (19, 2130), (20, 2200)],
            "STAF-DN400": [(3, 125), (3.5, 148), (4, 171), (4.5, 208), (5, 264), (5.5, 326), (6, 386), (6.5, 449), (7, 515), (7.5, 590), (8, 680), (9, 894), (10, 1140), (11, 1250), (12, 1400), (13, 1560), (14, 1730), (15, 1940), (16, 2140), (17, 2280), (18, 2410), (19, 2530), (20, 2630), (21, 2710), (22, 2780)],
            
            # STAF-SG - Variante STAF fonte GS (DN 65-400, grands réseaux, PN 16/25)
            # Source: STAF_STAF-SG_EN_MAIN.pdf - Mêmes valeurs Kv que STAF
            "STAF-SG-DN65": [(0.5, 1.02), (1, 2.39), (1.5, 3.77), (2, 5.18), (2.5, 6.52), (3, 8.18), (3.5, 11.6), (4, 18.6), (4.5, 29.9), (5, 39.6), (5.5, 47.9), (6, 57.5), (6.5, 66.3), (7, 74.2), (7.5, 80), (8, 85)],
            "STAF-SG-DN80": [(0.5, 2.33), (1, 4.25), (1.5, 6.20), (2, 8.47), (2.5, 11.4), (3, 15), (3.5, 20.8), (4, 29.9), (4.5, 43.3), (5, 57.5), (5.5, 69.6), (6, 81.2), (6.5, 92.8), (7, 104), (7.5, 114), (8, 123)],
            "STAF-SG-DN100": [(0.5, 2.54), (1, 5.59), (1.5, 8.64), (2, 11.5), (2.5, 15.5), (3, 26.2), (3.5, 42.8), (4, 66), (4.5, 91.7), (5, 108), (5.5, 119), (6, 136), (6.5, 151), (7, 164), (7.5, 174), (8, 185)],
            "STAF-SG-DN125": [(0.5, 5.99), (1, 10.9), (1.5, 15.7), (2, 21.5), (2.5, 29.1), (3, 37.5), (3.5, 54.2), (4, 85.2), (4.5, 118), (5, 148), (5.5, 168), (6, 198), (6.5, 232), (7, 255), (7.5, 275), (8, 294)],
            "STAF-SG-DN150": [(0.5, 5.39), (1, 13.3), (1.5, 22.8), (2, 41), (2.5, 65.7), (3, 92.6), (3.5, 127), (4, 176), (4.5, 214), (5, 249), (5.5, 281), (6, 307), (6.5, 332), (7, 353), (7.5, 374), (8, 400)],
            "STAF-SG-DN200": [(2, 40), (2.5, 50), (3, 65), (3.5, 90), (4, 120), (4.5, 165), (5, 225), (5.5, 285), (6, 340), (6.5, 400), (7, 435), (7.5, 470), (8, 515), (9, 595), (10, 650), (11, 710), (12, 765)],
            "STAF-SG-DN250": [(2, 90), (2.5, 110), (3, 140), (3.5, 195), (4, 255), (4.5, 320), (5, 385), (5.5, 445), (6, 500), (6.5, 545), (7, 590), (7.5, 660), (8, 725), (9, 820), (10, 940), (11, 1050), (12, 1185)],
            "STAF-SG-DN300": [(3, 150), (3.5, 230), (4, 300), (4.5, 370), (5, 450), (5.5, 535), (6, 620), (6.5, 690), (7, 750), (7.5, 815), (8, 890), (9, 970), (10, 1040), (11, 1120), (12, 1200), (13, 1320), (14, 1370), (15, 1400), (16, 1450)],
            "STAF-SG-DN350": [(3, 109), (3.5, 129), (4, 148), (4.5, 170), (5, 207), (5.5, 254), (6, 302), (6.5, 352), (7, 404), (7.5, 471), (8, 556), (9, 784), (10, 957), (11, 1100), (12, 1260), (13, 1420), (14, 1610), (15, 1760), (16, 1870), (17, 1960), (18, 2040), (19, 2130), (20, 2200)],
            "STAF-SG-DN400": [(3, 125), (3.5, 148), (4, 171), (4.5, 208), (5, 264), (5.5, 326), (6, 386), (6.5, 449), (7, 515), (7.5, 590), (8, 680), (9, 894), (10, 1140), (11, 1250), (12, 1400), (13, 1560), (14, 1730), (15, 1940), (16, 2140), (17, 2280), (18, 2410), (19, 2530), (20, 2630), (21, 2710), (22, 2780)],
            
            # STAF-R - Vanne d'équilibrage version « retour » (DN 65-200, PN 16/25)
            "STAF-R-DN65": [(0.5, 1.90), (1, 3.60), (1.5, 5.15), (2, 6.85), (2.5, 9.75), (3, 17.0), (3.5, 26.8), (4, 37.0), (4.5, 46.8), (5, 54.5), (5.5, 63.2), (6, 70.9), (6.5, 76.1), (7, 80.7), (7.5, 84.3), (8, 88.4)],
            "STAF-R-DN80": [(0.5, 2.10), (1, 4.20), (1.5, 6.30), (2, 8.40), (2.5, 11.6), (3, 14.7), (3.5, 20.5), (4, 30.3), (4.5, 43.2), (5, 57.5), (5.5, 70.9), (6, 83.8), (6.5, 96.1), (7, 108), (7.5, 118), (8, 125)],
            "STAF-R-DN100": [(0.5, 2.60), (1, 6.30), (1.5, 9.45), (2, 12.1), (2.5, 16.7), (3, 27.2), (3.5, 46.2), (4, 65.8), (4.5, 84.3), (5, 103), (5.5, 120), (6, 138), (6.5, 151), (7, 167), (7.5, 183), (8, 198)],
            "STAF-R-DN125": [(0.5, 5.80), (1, 11.0), (1.5, 16.2), (2, 22.6), (2.5, 28.3), (3, 37.5), (3.5, 57.6), (4, 86.9), (4.5, 119), (5, 147), (5.5, 174), (6, 206), (6.5, 229), (7, 259), (7.5, 287), (8, 314)],
            "STAF-R-DN150": [(0.5, 6.90), (1, 12.6), (1.5, 23.1), (2, 41.9), (2.5, 68.3), (3, 105), (3.5, 141), (4, 177), (4.5, 216), (5, 253), (5.5, 292), (6, 326), (6.5, 355), (7, 383), (7.5, 407), (8, 439)],
            "STAF-R-DN200": [(0.5, 10.3), (1, 20.0), (1.5, 34.9), (2, 56.5), (2.5, 84.3), (3, 121), (3.5, 165), (4, 214), (4.5, 269), (5, 329), (5.5, 393), (6, 460), (6.5, 532), (7, 608), (7.5, 689), (8, 773)],
            
            # STAG - Vanne grooved extrémités à gorge type Victaulic (DN 65-300, PN 16)
            "STAG-DN65": [(0.5, 1.90), (1, 3.60), (1.5, 5.15), (2, 6.85), (2.5, 9.75), (3, 17.0), (3.5, 26.8), (4, 37.0), (4.5, 46.8), (5, 54.5), (5.5, 63.2), (6, 70.9), (6.5, 76.1), (7, 80.7), (7.5, 84.3), (8, 88.4)],
            "STAG-DN80": [(0.5, 2.10), (1, 4.20), (1.5, 6.30), (2, 8.40), (2.5, 11.6), (3, 14.7), (3.5, 20.5), (4, 30.3), (4.5, 43.2), (5, 57.5), (5.5, 70.9), (6, 83.8), (6.5, 96.1), (7, 108), (7.5, 118), (8, 125)],
            "STAG-DN100": [(0.5, 2.60), (1, 6.30), (1.5, 9.45), (2, 12.1), (2.5, 16.7), (3, 27.2), (3.5, 46.2), (4, 65.8), (4.5, 84.3), (5, 103), (5.5, 120), (6, 138), (6.5, 151), (7, 167), (7.5, 183), (8, 198)],
            "STAG-DN125": [(0.5, 5.80), (1, 11.0), (1.5, 16.2), (2, 22.6), (2.5, 28.3), (3, 37.5), (3.5, 57.6), (4, 86.9), (4.5, 119), (5, 147), (5.5, 174), (6, 206), (6.5, 229), (7, 259), (7.5, 287), (8, 314)],
            "STAG-DN150": [(0.5, 6.90), (1, 12.6), (1.5, 23.1), (2, 41.9), (2.5, 68.3), (3, 105), (3.5, 141), (4, 177), (4.5, 216), (5, 253), (5.5, 292), (6, 326), (6.5, 355), (7, 383), (7.5, 407), (8, 439)],
            "STAG-DN200": [(0.5, 10.3), (1, 20.0), (1.5, 34.9), (2, 56.5), (2.5, 84.3), (3, 121), (3.5, 165), (4, 214), (4.5, 269), (5, 329), (5.5, 393), (6, 460), (6.5, 532), (7, 608), (7.5, 689), (8, 773)],
            "STAG-DN250": [(0.5, 13.9), (1, 37.0), (1.5, 69.9), (2, 113), (2.5, 167), (3, 230), (3.5, 304), (4, 389), (4.5, 483), (5, 588), (5.5, 703), (6, 829), (6.5, 964), (7, 1110), (7.5, 1266), (8, 1433)],
            "STAG-DN300": [(0.5, 21.6), (1, 51.3), (1.5, 91.5), (2, 142), (2.5, 203), (3, 273), (3.5, 354), (4, 446), (4.5, 548), (5, 660), (5.5, 782), (6, 914), (6.5, 1057), (7, 1210), (7.5, 1374), (8, 1548)],
            
            # STA - Ancienne vanne d'équilibrage TA (DN 15-150, maintenance/archive)
            "STA-DN15": [(0.5, 0.127), (1, 0.212), (1.5, 0.314), (2, 0.571), (2.5, 0.877), (3, 1.38), (3.5, 1.98), (4, 2.52)],
            "STA-DN20": [(0.5, 0.236), (1, 0.383), (1.5, 0.589), (2, 1.08), (2.5, 1.67), (3, 2.67), (3.5, 3.86), (4, 4.97)],
            "STA-DN25": [(0.5, 0.382), (1, 0.617), (1.5, 0.951), (2, 1.75), (2.5, 2.73), (3, 4.42), (3.5, 6.46), (4, 8.40)],
            "STA-DN32": [(0.5, 0.715), (1, 1.16), (1.5, 1.79), (2, 3.31), (2.5, 5.17), (3, 8.43), (3.5, 12.4), (4, 16.2)],
            "STA-DN40": [(0.5, 1.04), (1, 1.68), (1.5, 2.59), (2, 4.79), (2.5, 7.50), (3, 12.3), (3.5, 18.1), (4, 23.7)],
            "STA-DN50": [(0.5, 1.77), (1, 2.87), (1.5, 4.42), (2, 8.19), (2.5, 12.8), (3, 21.0), (3.5, 31.0), (4, 40.6)],
            "STA-DN65": [(0.5, 2.83), (1, 4.59), (1.5, 7.08), (2, 13.1), (2.5, 20.6), (3, 33.8), (3.5, 49.9), (4, 65.5), (4.5, 81.0), (5, 96.6)],
            "STA-DN80": [(0.5, 4.05), (1, 6.56), (1.5, 10.1), (2, 18.8), (2.5, 29.5), (3, 48.4), (3.5, 71.5), (4, 93.9), (4.5, 116), (5, 139)],
            "STA-DN100": [(0.5, 6.30), (1, 10.2), (1.5, 15.8), (2, 29.3), (2.5, 45.9), (3, 75.3), (3.5, 111), (4, 146), (4.5, 181), (5, 216)],
            "STA-DN125": [(0.5, 11.0), (1, 17.8), (1.5, 27.5), (2, 50.9), (2.5, 79.7), (3, 131), (3.5, 193), (4, 253), (4.5, 314), (5, 374)],
            "STA-DN150": [(0.5, 12.6), (1, 20.4), (1.5, 31.5), (2, 58.3), (2.5, 91.3), (3, 150), (3.5, 221), (4, 290), (4.5, 359), (5, 429)],
            
            # MDFO - Orifice fixe de mesure (DN 20-900, équilibrage + mesure TA-Scope)
            # Note: Kv fixe, pas de tours (orifice calibré)
            "MDFO-DN20": [(0, 3.8)],
            "MDFO-DN25": [(0, 6.1)],
            "MDFO-DN32": [(0, 10.0)],
            "MDFO-DN40": [(0, 14.5)],
            "MDFO-DN50": [(0, 24.8)],
            "MDFO-DN65": [(0, 40.0)],
            "MDFO-DN80": [(0, 57.0)],
            "MDFO-DN100": [(0, 89.0)],
            "MDFO-DN125": [(0, 140)],
            "MDFO-DN150": [(0, 200)],
            "MDFO-DN200": [(0, 360)],
            "MDFO-DN250": [(0, 560)],
            "MDFO-DN300": [(0, 810)],
            "MDFO-DN350": [(0, 1100)],
            "MDFO-DN400": [(0, 1440)],
            "MDFO-DN450": [(0, 1820)],
            "MDFO-DN500": [(0, 2240)],
            "MDFO-DN600": [(0, 3230)],
            "MDFO-DN700": [(0, 4400)],
            "MDFO-DN800": [(0, 5750)],
            "MDFO-DN900": [(0, 7270)],
            
            # STAP - Régulateur de pression différentielle pour équilibrage dynamique (DN 15-100)
            # Note: Kv max à pleine ouverture (régulateur de ΔP automatique)
            "STAP-DN15": [(0, 2.5)],
            "STAP-DN20": [(0, 4.0)],
            "STAP-DN25": [(0, 6.3)],
            "STAP-DN32": [(0, 10.0)],
            "STAP-DN40": [(0, 16.0)],
            "STAP-DN50": [(0, 25.0)],
            "STAP-DN65": [(0, 40.0)],
            "STAP-DN80": [(0, 63.0)],
            "STAP-DN100": [(0, 100.0)],
            
            # STAM - Régulateur de pression différentielle pour boucles et colonnes (DN 15-50)
            # Note: Kv max à pleine ouverture (régulateur de ΔP pour boucles)
            "STAM-DN15": [(0, 2.5)],
            "STAM-DN20": [(0, 4.0)],
            "STAM-DN25": [(0, 6.3)],
            "STAM-DN32": [(0, 10.0)],
            "STAM-DN40": [(0, 16.0)],
            "STAM-DN50": [(0, 25.0)],
            
            # STAZ / STAP-R - Variantes anciennes pour rétrofits (DN 15-50, archives IMI Hydronic)
            # Note: Kv max à pleine ouverture (régulateurs legacy)
            "STAZ-DN15": [(0, 2.5)],
            "STAZ-DN20": [(0, 4.0)],
            "STAZ-DN25": [(0, 6.3)],
            "STAZ-DN32": [(0, 10.0)],
            "STAZ-DN40": [(0, 16.0)],
            "STAZ-DN50": [(0, 25.0)],
            "STAP-R-DN15": [(0, 2.5)],
            "STAP-R-DN20": [(0, 4.0)],
            "STAP-R-DN25": [(0, 6.3)],
            "STAP-R-DN32": [(0, 10.0)],
            "STAP-R-DN40": [(0, 16.0)],
            "STAP-R-DN50": [(0, 25.0)],
            
           
        }

        self.diametres = [
            # STAD - Vanne d'équilibrage manuelle filetée (PN 25)
            "STAD-DN10", "STAD-DN15", "STAD-DN20", "STAD-DN25", "STAD-DN32", "STAD-DN40", "STAD-DN50",
            # STAV - Vanne d'équilibrage Venturi filetée (PN 20)
            "STAV-DN15", "STAV-DN20", "STAV-DN25", "STAV-DN32", "STAV-DN40", "STAV-DN50",
            # TBV - Vanne terminale d'équilibrage manuelle (unités terminales)
            "TBV-DN15", "TBV-DN20",
            # TBV-C - Vanne terminale équilibrage + contrôle (avec TA-Scope)
            "TBV-C-DN10", "TBV-C-DN15", "TBV-C-DN20",
            # TBV abaques - Variantes à positions numérotées (1-10) selon documentation IMI TA
            "TBV-LF-DN15", "TBV-NF-DN15", "TBV-NF-DN20",
            # STAF - Vanne d'équilibrage à brides fonte (réseaux principaux, PN 16/25)
            "STAF-DN20", "STAF-DN25", "STAF-DN32", "STAF-DN40", "STAF-DN50", 
            "STAF-DN65", "STAF-DN80", "STAF-DN100", "STAF-DN125", "STAF-DN150",
            "STAF-DN200", "STAF-DN250", "STAF-DN300", "STAF-DN350", "STAF-DN400",
            # STAF-SG - Variante STAF fonte GS (DN 65-400, grands réseaux, PN 16/25)
            "STAF-SG-DN65", "STAF-SG-DN80", "STAF-SG-DN100", "STAF-SG-DN125", "STAF-SG-DN150",
            "STAF-SG-DN200", "STAF-SG-DN250", "STAF-SG-DN300", "STAF-SG-DN350", "STAF-SG-DN400",
            # STAF-R - Vanne d'équilibrage version « retour » (DN 65-200, PN 16/25)
            "STAF-R-DN65", "STAF-R-DN80", "STAF-R-DN100", "STAF-R-DN125", "STAF-R-DN150", "STAF-R-DN200",
            # STAG - Vanne grooved extrémités à gorge type Victaulic (DN 65-300, PN 16)
            "STAG-DN65", "STAG-DN80", "STAG-DN100", "STAG-DN125", "STAG-DN150", "STAG-DN200", "STAG-DN250", "STAG-DN300",
            # STA - Ancienne vanne d'équilibrage TA (DN 15-150, maintenance/archive)
            "STA-DN15", "STA-DN20", "STA-DN25", "STA-DN32", "STA-DN40", "STA-DN50", "STA-DN65", "STA-DN80", "STA-DN100", "STA-DN125", "STA-DN150",
            # MDFO - Orifice fixe de mesure (DN 20-900, équilibrage + mesure TA-Scope, Kv fixe)
            "MDFO-DN20", "MDFO-DN25", "MDFO-DN32", "MDFO-DN40", "MDFO-DN50", "MDFO-DN65", "MDFO-DN80", "MDFO-DN100",
            "MDFO-DN125", "MDFO-DN150", "MDFO-DN200", "MDFO-DN250", "MDFO-DN300", "MDFO-DN350", "MDFO-DN400",
            "MDFO-DN450", "MDFO-DN500", "MDFO-DN600", "MDFO-DN700", "MDFO-DN800", "MDFO-DN900",
            # STAP - Régulateur de pression différentielle équilibrage dynamique (DN 15-100, Kv max)
            "STAP-DN15", "STAP-DN20", "STAP-DN25", "STAP-DN32", "STAP-DN40", "STAP-DN50", "STAP-DN65", "STAP-DN80", "STAP-DN100",
            # STAM - Régulateur de pression différentielle boucles/colonnes (DN 15-50, Kv max)
            "STAM-DN15", "STAM-DN20", "STAM-DN25", "STAM-DN32", "STAM-DN40", "STAM-DN50",
            # STAZ / STAP-R - Régulateurs ΔP anciennes variantes pour rétrofits (DN 15-50, archives, Kv max)
            "STAZ-DN15", "STAZ-DN20", "STAZ-DN25", "STAZ-DN32", "STAZ-DN40", "STAZ-DN50",
            "STAP-R-DN15", "STAP-R-DN20", "STAP-R-DN25", "STAP-R-DN32", "STAP-R-DN40", "STAP-R-DN50",
            
        ]

    def on_pressure_change(self):
        """Callback appelé lorsque self.Outlet.P change."""
        if hasattr(self, '_calculating_inverse'):
            return  # Éviter les boucles infinies
        self._calculating_inverse = True
        try:
            self.calculate_inverse()
        finally:
            delattr(self, '_calculating_inverse')
    
    def calculate(self):
        """
        Calcule la perte de charge en fonction du débit (q en m3/h),
        du nombre de tours et du diamètre nominal (DN).
        Mode direct : calcule la pression de sortie à partir de la pression d'entrée.
        """
        self.rho = PropsSI('D', 'P', self.Inlet.P, 'H', self.Inlet.h, self.Inlet.fluid)
        #convertir le débit de kg/s à m3/h
        self.q=self.Inlet.F*3600/self.rho # Débit en m3/h

        # Calculer Kv
        kv = self.get_kv_value()
        
        self.delta_P = (self.q / kv) ** 2*10**5 # Formule : ΔP = (q / Kv)²  en Pa

        self.Inlet.calculate_properties()
        
        # Désactiver temporairement le callback pour éviter les boucles infinies
        original_callback = self.Outlet.callback
        self.Outlet.callback = None
        
        self.Outlet.P=self.Inlet.P-self.delta_P
        self.Outlet.F=self.Inlet.F
        self.Outlet.fluid = self.Inlet.fluid
        self.Outlet.T = self.Inlet.T
        self.Outlet.h = self.Inlet.h  # Transmettre l'enthalpie
        self.Outlet.calculate_properties()
        
        # Réactiver le callback
        self.Outlet.callback = original_callback

        # Stocker les données dans un DataFrame
        self.df = pd.DataFrame({
            'Débit (m3/h)': [self.q],
            'Nombre de tours': [self.nb_tours],
            'Diamètre nominal (DN)': [self.dn],
            'Kv': [kv],
            'Pression d\'entrée (Pa)': [self.Inlet.P],
            'Perte de charge (Pa)': [self.delta_P],  
            'Pression de sortie (Pa)': [self.Outlet.P],
        }).T

    def calculate_inverse(self):
        """
        Calcule la pression d'entrée en fonction de la pression de sortie.
        Mode inverse : utilisé quand la pression de sortie est imposée par un autre composant.
        """
        if self.Outlet.P is None or self.Inlet.F is None or self.nb_tours is None or self.dn is None:
            return  # Pas assez d'informations pour le calcul inverse
        
        # Calculer la densité avec les propriétés d'entrée actuelles si disponibles
        if self.Inlet.P is not None and self.Inlet.h is not None and self.Inlet.fluid is not None:
            self.rho = PropsSI('D', 'P', self.Inlet.P, 'H', self.Inlet.h, self.Inlet.fluid)
        else:
            # Estimation avec la pression de sortie si pas d'autres infos
            if self.Inlet.fluid is not None:
                self.rho = PropsSI('D', 'P', self.Outlet.P, 'T', 298.15, self.Inlet.fluid)
            else:
                return
        
        #convertir le débit de kg/s à m3/h
        self.q = self.Inlet.F * 3600 / self.rho  # Débit en m3/h

        # Calculer Kv
        kv = self.get_kv_value()
        
        self.delta_P = (self.q / kv) ** 2 * 10**5  # Formule : ΔP = (q / Kv)²  en Pa
        
        # Calculer la nouvelle pression d'entrée à partir de la pression de sortie
        new_inlet_P = self.Outlet.P + self.delta_P
        
        # Mettre à jour la pression d'entrée ET déclencher la propagation
        original_inlet_callback = getattr(self.Inlet, 'callback', None)
        self.Inlet.callback = None
        self.Inlet.P = new_inlet_P
        self.Inlet.callback = original_inlet_callback
        
        # Déclencher manuellement le callback pour propager la nouvelle pression
        if original_inlet_callback:
            original_inlet_callback()
        
        # Mettre à jour les propriétés de fluide
        self.Outlet.F = self.Inlet.F
        self.Outlet.fluid = self.Inlet.fluid
        self.Outlet.h = self.Inlet.h  # Transmettre l'enthalpie
        if self.Inlet.T is not None:
            self.Outlet.T = self.Inlet.T
        
        # Recalculer les propriétés
        self.Inlet.calculate_properties()
        self.Outlet.calculate_properties()

        # Stocker les données dans un DataFrame
        self.df = pd.DataFrame({
            'Débit (m3/h)': [self.q],
            'Nombre de tours': [self.nb_tours],
            'Diamètre nominal (DN)': [self.dn],
            'Kv': [kv],
            'Pression d\'entrée (Pa)': [self.Inlet.P],
            'Perte de charge (Pa)': [self.delta_P],  
            'Pression de sortie (Pa)': [self.Outlet.P],
        }).T

    def get_kv_value(self):
        """
        Obtient la valeur Kv en fonction du DN et du nombre de tours.
        """
        # Normaliser le DN en string si nécessaire
        dn_key = self.dn if isinstance(self.dn, str) else f"DN{self.dn}"
        
        if dn_key not in self.kv_values:
            raise ValueError(f"Diamètre nominal non valide: {self.dn}")
        
        # Rechercher la valeur Kv correspondant au nombre de tours
        # Si la valeur exacte n'existe pas, interpoler linéairement entre les deux valeurs encadrantes
        kv_data = self.kv_values[dn_key]
        kv = None
        
        # Chercher d'abord une correspondance exacte
        for ouverture, kv_val in kv_data:
            if ouverture == self.nb_tours:
                kv = kv_val
                break
        
        # Si pas de correspondance exacte, interpoler linéairement
        if kv is None:
            # Trier les données par ouverture
            kv_data_sorted = sorted(kv_data, key=lambda x: x[0])
            
            # Trouver les deux points encadrants
            ouverture_inf = None
            kv_inf = None
            ouverture_sup = None
            kv_sup = None
            
            for i, (ouverture, kv_val) in enumerate(kv_data_sorted):
                if ouverture < self.nb_tours:
                    ouverture_inf = ouverture
                    kv_inf = kv_val
                elif ouverture > self.nb_tours:
                    ouverture_sup = ouverture
                    kv_sup = kv_val
                    break
            
            # Vérifier qu'on a bien deux points pour interpoler
            if ouverture_inf is not None and ouverture_sup is not None:
                # Interpolation linéaire: Kv = Kv_inf + (Kv_sup - Kv_inf) * (nb_tours - ouverture_inf) / (ouverture_sup - ouverture_inf)
                kv = kv_inf + (kv_sup - kv_inf) * (self.nb_tours - ouverture_inf) / (ouverture_sup - ouverture_inf)
            else:
                raise ValueError(f"Nombre de tours hors limites pour {dn_key}: {self.nb_tours}. Plage disponible: {kv_data_sorted[0][0]} - {kv_data_sorted[-1][0]}")
        
        return kv
    
    def Plot(self):
        """
        Trace le point de fonctionnement de la vanne sur la courbe de réseau.
        La courbe de réseau montre delta_P (Pa) en fonction du débit (m3/h)
        pour des vitesses d'écoulement de 0 à 2 m/s basées sur le DN de la vanne.
        """
        if self.dn is None or self.nb_tours is None:
            raise ValueError("Le DN et le nombre de tours doivent être définis avant de tracer le graphique")
        
        # Extraire le DN numérique du format "STAD-DN15", "STAV-DN20", etc.
        dn_str = self.dn
        if isinstance(dn_str, str):
            # Extraire le nombre après "DN"
            import re
            match = re.search(r'DN(\d+)', dn_str)
            if match:
                dn_mm = int(match.group(1))
            else:
                raise ValueError(f"Impossible d'extraire le DN numérique de {dn_str}")
        else:
            dn_mm = int(dn_str)
        
        # Diamètre intérieur en mètres (approximation: DN en mm ≈ diamètre intérieur)
        d_m = dn_mm / 1000.0
        
        # Section de passage en m²
        section = math.pi * (d_m ** 2) / 4
        
        # Obtenir le Kv actuel
        kv = self.get_kv_value()
        
        # Générer la courbe de réseau pour des vitesses de 0 à 3 m/s
        vitesses = np.linspace(0, 3, 100)  # Vitesses de 0 à 3 m/s
        debits_reseau = vitesses * section * 3600  # Débit en m3/h
        delta_p_reseau = (debits_reseau / kv) ** 2 * 10**5  # ΔP en Pa
        
        # Point de fonctionnement actuel
        if self.q is not None and self.delta_P is not None:
            q_actuel = self.q
            delta_p_actuel = self.delta_P
        else:
            raise ValueError("Calculer d'abord le point de fonctionnement avec calculate() ou calculate_inverse()")
        
        # Créer le graphique
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Tracer la courbe de réseau sur l'axe principal (kPa)
        ax1.plot(debits_reseau, delta_p_reseau / 1000, 'b-', linewidth=2, label=f'Courbe de réseau {self.dn} ({self.nb_tours} tours, Kv={kv:.2f})')
        
        # Tracer le point de fonctionnement
        ax1.plot(q_actuel, delta_p_actuel / 1000, 'ro', markersize=10, label=f'Point de fonctionnement ({q_actuel:.2f} m³/h, {delta_p_actuel/1000:.2f} kPa)')
        
        # Ajouter des lignes de référence pour les vitesses
        vitesses_ref = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        for v in vitesses_ref:
            q_ref = v * section * 3600
            ax1.axvline(x=q_ref, color='gray', linestyle='--', alpha=0.3)
            ax1.text(q_ref, ax1.get_ylim()[1] * 0.5, f'{v} m/s', rotation=90, verticalalignment='center', fontsize=8, color='gray')
        
        # Configuration de l'axe principal (kPa)
        ax1.set_xlabel('Débit (m³/h)', fontsize=12)
        ax1.set_ylabel('Perte de charge (kPa)', fontsize=12, color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.set_title(f'Courbe de réseau - Vanne TA {self.dn}', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left', fontsize=10)
        
        # Créer un axe secondaire (bar)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Perte de charge (bar)', fontsize=12, color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        # Synchroniser les limites des deux axes (1 bar = 100 kPa)
        y1_min, y1_max = ax1.get_ylim()
        ax2.set_ylim(y1_min / 100, y1_max / 100)
        
        # Afficher les informations techniques en bas à droite
        info_text = f'DN: {dn_mm} mm\nSection: {section*10000:.2f} cm²\nVitesse actuelle: {q_actuel/(section*3600):.2f} m/s'
        ax1.text(0.98, 0.02, info_text, transform=ax1.transAxes, 
                fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.tight_layout()
        plt.show()
        
        return fig
    

