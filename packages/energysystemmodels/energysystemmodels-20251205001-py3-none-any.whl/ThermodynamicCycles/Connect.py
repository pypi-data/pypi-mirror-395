from ThermodynamicCycles.FluidPort.FluidPort import FluidPort
import uuid

# Dictionnaire global pour gérer les nœuds hydrauliques
_hydraulic_nodes = {}

def Fluid_connect(inlet=FluidPort(), outlet=FluidPort()):
    # Ajouter cette connexion aux listes de connexions
    if inlet not in outlet.connected_inlets:
        outlet.connected_inlets.append(inlet)
    if outlet not in inlet.connected_outlets:
        inlet.connected_outlets.append(outlet)
    
    # Copier les propriétés du fluide (seulement si définies dans outlet)
    if outlet.fluid is not None:
        inlet.fluid = outlet.fluid
    if outlet.h is not None:
        inlet.h = outlet.h
    if outlet.F is not None:
        inlet.F = outlet.F
    if outlet.S is not None:
        inlet.S = outlet.S
    if outlet.T is not None:
        inlet.T = outlet.T
    
    # Gérer les pressions avec propagation des callbacks
    if inlet.P is not None:
        outlet.P = inlet.P
    else:
        inlet.P = outlet.P
    
    # Créer ou mettre à jour le nœud hydraulique
    node_id = _create_or_update_hydraulic_node(inlet, outlet)
    
    # Sauvegarder les callbacks originaux
    original_inlet_callback = getattr(inlet, 'callback', None)
    original_outlet_callback = getattr(outlet, 'callback', None)
    
    # Créer une référence croisée pour la synchronisation
    inlet._connected_port = outlet
    outlet._connected_port = inlet
    
    # Créer des callbacks qui appliquent la loi de Kirchhoff
    def inlet_kirchhoff_callback():
        if original_inlet_callback:
            original_inlet_callback()
        _apply_kirchhoff_law(inlet)
    
    def outlet_kirchhoff_callback():
        if original_outlet_callback:
            original_outlet_callback()
        _apply_kirchhoff_law(outlet)
    
    # Assigner les nouveaux callbacks
    inlet.callback = inlet_kirchhoff_callback
    outlet.callback = outlet_kirchhoff_callback
    
    # Calculer les propriétés
    inlet.calculate_properties()
    outlet.calculate_properties()
    
    return "connectés"

def _create_or_update_hydraulic_node(inlet, outlet):
    """Crée ou met à jour un nœud hydraulique pour gérer les connexions multiples."""
    
    # Chercher si l'un des ports appartient déjà à un nœud
    existing_node_id = None
    
    # L'outlet est potentiellement un point de jonction (plusieurs inlets connectés)
    if hasattr(outlet, 'node_id') and outlet.node_id and outlet.node_id in _hydraulic_nodes:
        existing_node_id = outlet.node_id
    # L'inlet est potentiellement un point de jonction (plusieurs outlets connectés) 
    elif hasattr(inlet, 'node_id') and inlet.node_id and inlet.node_id in _hydraulic_nodes:
        existing_node_id = inlet.node_id
    
    # Si on trouve un nœud existant, y ajouter les ports
    if existing_node_id:
        node = _hydraulic_nodes[existing_node_id]
        
        # Ajouter l'inlet comme une nouvelle branche sortante du nœud
        if inlet not in node['branches_out']:
            node['branches_out'].append(inlet)
            inlet.node_id = existing_node_id
        
        # L'outlet reste le point central du nœud
        if outlet not in node['center_ports']:
            node['center_ports'].append(outlet)
            outlet.node_id = existing_node_id
            
        print(f"🔗 Nœud existant {existing_node_id[:8]}... étendu: centre={len(node['center_ports'])}, branches={len(node['branches_out'])}")
        return existing_node_id
    
    # Sinon, créer un nouveau nœud
    else:
        node_id = str(uuid.uuid4())
        _hydraulic_nodes[node_id] = {
            'center_ports': [outlet],  # Le port de sortie du composant amont (ex: PUMP.Outlet)
            'branches_out': [inlet],   # Les ports d'entrée des composants aval (ex: VALVE.Inlet)
            'pressure': outlet.P or inlet.P
        }
        inlet.node_id = node_id
        outlet.node_id = node_id
        print(f"🆕 Nouveau nœud {node_id[:8]}... créé: 1 centre, 1 branche")
        return node_id

def _apply_kirchhoff_law(port):
    """Applique la loi de Kirchhoff (conservation de débit et homogénéité de pression) au nœud."""
    if not port.node_id or port.node_id not in _hydraulic_nodes:
        return
    
    node = _hydraulic_nodes[port.node_id]
    
    # Éviter les boucles infinies
    if hasattr(port, '_applying_kirchhoff'):
        return
    
    try:
        port._applying_kirchhoff = True
        
        # 1. HOMOGÉNÉITÉ DES PRESSIONS : tous les ports du nœud ont la même pression
        # PRIORITÉ: Le port qui a déclenché le callback a la priorité
        # Cela permet à la pression imposée en aval (ex: SINK) de remonter correctement en amont
        target_pressure = port.P  # Le port qui vient de changer
        
        if target_pressure is not None:
            # Égaliser les pressions des ports centraux (ex: PUMP.Outlet ou VALVE.Outlet)
            for center_port in node['center_ports']:
                if center_port.P != target_pressure:
                    old_P_str = f"{center_port.P/100000:.3f}" if center_port.P is not None else "None"
                    print(f"🔧 NŒUD KIRCHHOFF: Égalisation pression centre {old_P_str}→{target_pressure/100000:.3f} bar")
                    # Désactiver temporairement le callback pour éviter les boucles
                    original_callback = center_port.callback
                    center_port.callback = None
                    center_port.P = target_pressure
                    center_port.callback = original_callback
                    # Appeler manuellement le callback original APRÈS l'égalisation
                    if original_callback:
                        original_callback()
            
            # Égaliser les pressions des branches sortantes (ex: VALVE.Inlet ou SINK.Inlet)
            for branch_port in node['branches_out']:
                if branch_port.P != target_pressure:
                    old_P_str = f"{branch_port.P/100000:.3f}" if branch_port.P is not None else "None"
                    print(f"🔧 NŒUD KIRCHHOFF: Égalisation pression branche {old_P_str}→{target_pressure/100000:.3f} bar")
                    # Désactiver temporairement le callback pour éviter les boucles
                    original_callback = branch_port.callback
                    branch_port.callback = None
                    branch_port.P = target_pressure
                    branch_port.callback = original_callback
                    # Appeler manuellement le callback original APRÈS l'égalisation
                    if original_callback:
                        original_callback()
            
            node['pressure'] = target_pressure
        
        # 2. CONSERVATION DU DÉBIT : Débit centre = Σ débits branches
        center_flow = sum(center.F for center in node['center_ports'] if center.F is not None)
        branches_flow = sum(branch.F for branch in node['branches_out'] if branch.F is not None)
        
        if center_flow > 0 and branches_flow > 0:
            flow_imbalance = center_flow - branches_flow
            if abs(flow_imbalance) > 0.001:  # Seuil de tolérance
                print(f"⚠️  NŒUD KIRCHHOFF: Déséquilibre débit détecté: {flow_imbalance:.3f} kg/s")
                print(f"   Débit centre: {center_flow:.3f} kg/s")
                print(f"   Débit branches: {branches_flow:.3f} kg/s")
                
                # SPLITTER : redistribution proportionnelle dans les branches
                if len(node['branches_out']) > 1 and branches_flow > 0:
                    print("   🔄 SPLITTER: redistribution proportionnelle du débit:")
                    for branch_port in node['branches_out']:
                        if branch_port.F is not None and branch_port.F > 0:
                            ratio = branch_port.F / branches_flow
                            new_flow = center_flow * ratio
                            print(f"     {branch_port.F:.3f}→{new_flow:.3f} kg/s (ratio: {ratio:.2f})")
                            branch_port._F = new_flow
                
                # COLLECTEUR : ajustement du débit central
                elif len(node['center_ports']) == 1 and len(node['branches_out']) > 1:
                    center_port = node['center_ports'][0]
                    print(f"   🔄 COLLECTEUR: ajustement débit centre: {center_port.F:.3f}→{branches_flow:.3f} kg/s")
                    center_port._F = branches_flow
    
    finally:
        delattr(port, '_applying_kirchhoff')

def get_node_info(port):
    """Retourne les informations du nœud hydraulique d'un port."""
    if not port.node_id or port.node_id not in _hydraulic_nodes:
        return None
    
    node = _hydraulic_nodes[port.node_id]
    return {
        'node_id': port.node_id,
        'inlets': len(node['center_ports']),  # Ports d'entrée (centres)
        'outlets': len(node['branches_out']), # Ports de sortie (branches)
        'pressure': node['pressure'],
        'total_flow_in': sum(center.F for center in node['center_ports'] if center.F is not None),
        'total_flow_out': sum(branch.F for branch in node['branches_out'] if branch.F is not None)
    }