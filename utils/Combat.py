# utils/combat.py

def check_hit(attacker, defender):
    """
    Retorna True si el atacante está en animación de ataque
    y su rango alcanza al defensor.
    """
    if not attacker.is_attacking:
        return False

    if not defender.is_alive:
        return False

    dist = abs(attacker.x - defender.x)

    # Tomamos el rango del ataque actual
    current_action = attacker.action
    attack_data = next(
        (a for a in attacker.attacks if a['action'] == current_action),
        None
    )
    if attack_data is None:
        return False

    return dist <= attack_data['range']