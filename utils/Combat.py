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

def check_projectile_hits(attacker, defender):
    """
    Revisa si algún proyectil del atacante colisiona con el defensor.
    Solo aplica si el atacante tiene proyectiles (Mage).
    Retorna el daño total recibido (0 si no hay colisión).
    """
    if not hasattr(attacker, 'projectiles'):
        return 0
    if not defender.is_alive:
        return 0

    total_damage = 0
    for proj in attacker.projectiles:
        if not proj.active:
            continue
        if proj.rect.colliderect(defender.rect):
            total_damage += proj.damage
            proj.active = False   # desaparece al colisionar

    return total_damage