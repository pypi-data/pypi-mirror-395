import pandas as pd
from HeatTransfer import PlateHeatTransfer

class Object:
    """
    Classe pour calculer le transfert de chaleur d'un corps parallélépipédique rectangulaire.
    
    Paramètres:
    -----------
    L : float
        Longueur en mètres (axe X)
    W : float
        Largeur en mètres (axe Y)
    H : float
        Hauteur en mètres (axe Z)
    Ta : float
        Température ambiante en °C
    faces_config : dict
        Configuration des faces avec structure:
        {
            'top': {'Tp': float, 'isolated': bool},
            'bottom': {'Tp': float, 'isolated': bool},
            'front': {'Tp': float, 'isolated': bool},
            'back': {'Tp': float, 'isolated': bool},
            'left': {'Tp': float, 'isolated': bool},
            'right': {'Tp': float, 'isolated': bool}
        }
    """
    
    def __init__(self, L, W, H, Ta, faces_config=None):
        self.L = L  # Longueur (X)
        self.W = W  # Largeur (Y)
        self.H = H  # Hauteur (Z)
        self.Ta = Ta
        
        # Configuration par défaut si non spécifiée
        if faces_config is None:
            default_Tp = Ta + 35
            faces_config = {
                'top': {'Tp': default_Tp, 'isolated': False},
                'bottom': {'Tp': default_Tp, 'isolated': False},
                'front': {'Tp': default_Tp, 'isolated': False},
                'back': {'Tp': default_Tp, 'isolated': False},
                'left': {'Tp': default_Tp, 'isolated': False},
                'right': {'Tp': default_Tp, 'isolated': False}
            }
        
        self.faces_config = faces_config
        self.results = {}
        self.df = None
        
    def calculate(self):
        """
        Calcule le transfert de chaleur pour toutes les faces.
        """
        # Face supérieure (horizontal_up)
        if not self.faces_config['top']['isolated']:
            self.results['top'] = PlateHeatTransfer.Object(
                orientation='horizontal_up',
                Tp=self.faces_config['top']['Tp'],
                Ta=self.Ta,
                W=self.W,
                L=self.L
            ).calculate()
        else:
            self.results['top'] = 0.0
        
        # Face inférieure (horizontal_down)
        if not self.faces_config['bottom']['isolated']:
            self.results['bottom'] = PlateHeatTransfer.Object(
                orientation='horizontal_down',
                Tp=self.faces_config['bottom']['Tp'],
                Ta=self.Ta,
                W=self.W,
                L=self.L
            ).calculate()
        else:
            self.results['bottom'] = 0.0
        
        # Face avant (vertical, W x H)
        if not self.faces_config['front']['isolated']:
            self.results['front'] = PlateHeatTransfer.Object(
                orientation='vertical',
                Tp=self.faces_config['front']['Tp'],
                Ta=self.Ta,
                W=self.W,
                H=self.H
            ).calculate()
        else:
            self.results['front'] = 0.0
        
        # Face arrière (vertical, W x H)
        if not self.faces_config['back']['isolated']:
            self.results['back'] = PlateHeatTransfer.Object(
                orientation='vertical',
                Tp=self.faces_config['back']['Tp'],
                Ta=self.Ta,
                W=self.W,
                H=self.H
            ).calculate()
        else:
            self.results['back'] = 0.0
        
        # Face gauche (vertical, L x H)
        if not self.faces_config['left']['isolated']:
            self.results['left'] = PlateHeatTransfer.Object(
                orientation='vertical',
                Tp=self.faces_config['left']['Tp'],
                Ta=self.Ta,
                W=self.L,
                H=self.H
            ).calculate()
        else:
            self.results['left'] = 0.0
        
        # Face droite (vertical, L x H)
        if not self.faces_config['right']['isolated']:
            self.results['right'] = PlateHeatTransfer.Object(
                orientation='vertical',
                Tp=self.faces_config['right']['Tp'],
                Ta=self.Ta,
                W=self.L,
                H=self.H
            ).calculate()
        else:
            self.results['right'] = 0.0
        
        # Créer le DataFrame
        self._create_dataframe()
        
        return self.results
    
    def _create_dataframe(self):
        """
        Crée un DataFrame pandas avec les résultats.
        """
        data = []
        
        for face_name, heat_transfer in self.results.items():
            face_config = self.faces_config[face_name]
            
            # Calcul de la surface
            if face_name in ['top', 'bottom']:
                surface = self.L * self.W
            elif face_name in ['front', 'back']:
                surface = self.W * self.H
            else:  # left, right
                surface = self.L * self.H
            
            data.append({
                'Face': face_name,
                'Orientation': self._get_orientation(face_name),
                'Surface (m²)': round(surface, 4),
                'Tp (°C)': face_config['Tp'],
                'Ta (°C)': self.Ta,
                'ΔT (°C)': face_config['Tp'] - self.Ta,
                'Isolated': face_config['isolated'],
                'Heat Transfer (W)': round(heat_transfer, 2),
                'Heat Flux (W/m²)': round(heat_transfer / surface, 2) if surface > 0 else 0
            })
        
        # Ajouter une ligne pour le total
        total_heat = sum(self.results.values())
        total_surface = 2 * (self.L * self.W + self.W * self.H + self.L * self.H)
        
        data.append({
            'Face': 'TOTAL',
            'Orientation': '-',
            'Surface (m²)': round(total_surface, 4),
            'Tp (°C)': '-',
            'Ta (°C)': self.Ta,
            'ΔT (°C)': '-',
            'Isolated': '-',
            'Heat Transfer (W)': round(total_heat, 2),
            'Heat Flux (W/m²)': round(total_heat / total_surface, 2) if total_surface > 0 else 0
        })
        
        self.df = pd.DataFrame(data)
    
    def _get_orientation(self, face_name):
        """
        Retourne l'orientation de la face.
        """
        orientations = {
            'top': 'Horizontal (up)',
            'bottom': 'Horizontal (down)',
            'front': 'Vertical',
            'back': 'Vertical',
            'left': 'Vertical',
            'right': 'Vertical'
        }
        return orientations.get(face_name, 'Unknown')
    
    def get_total_heat_transfer(self):
        """
        Retourne le transfert de chaleur total.
        """
        return sum(self.results.values())
    
    def print_summary(self):
        """
        Affiche un résumé des résultats.
        """
        if self.df is not None:
            print("\n" + "="*80)
            print(f"TRANSFERT DE CHALEUR - CORPS PARALLÉLÉPIPÉDIQUE")
            print("="*80)
            print(f"Dimensions: L={self.L}m x W={self.W}m x H={self.H}m")
            print(f"Température ambiante: {self.Ta}°C")
            print("="*80)
            print(self.df.to_string(index=False))
            print("="*80)
