def check_hit(attacker, defender):
    if not attacker.is_attacking:
        return False
    if not defender.is_alive:
        return False
    if attacker.hit_landed:
        return False

    dist = abs(attacker.x - defender.x)
    current_action = attacker.action
    attack_data = next(
        (a for a in attacker.attacks if a['action'] == current_action),
        None
    )
    if attack_data is None:
        return False

    if dist <= attack_data['range']:
        attacker.hit_landed = True
        return True

    return False