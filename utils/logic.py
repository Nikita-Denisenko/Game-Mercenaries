def calculate_distance(attackers_location, defenders_location):
    if attackers_location == defenders_location:
        return 0

    if defenders_location.location_id in attackers_location.unavailable_locations:
        distance = 3
    elif defenders_location.location_id in attackers_location.distant_locations:
        distance = 2
    else:
        distance = 1

    if attackers_location.location_id == "7":
        distance -= attackers_location.rules["cut_distance_bonus"]

    return distance


def calculate_accuracy(attacker, defender, weapon, laser_sight, camouflage, distance):
    accuracy = weapon.accuracy
    accuracy -= distance
    if weapon.weapon_type != "Холодное оружие":
        if attacker.unit.unit_id == "4":
            accuracy += attacker.unit.rules["accuracy_bonus"]
        if laser_sight in attacker.inventory:
            accuracy += laser_sight.rules["accuracy_bonus"]
    if defender.unit.unit_id == "3":
        accuracy -= defender.unit.rules["cut_enemy_accuracy"]
    elif camouflage in defender.inventory:
        accuracy -= camouflage.rules["cut_enemy_accuracy"]
    return accuracy


def calculate_damage(defender, weapon, armor):
    damage = weapon.damage
    if weapon.weapon_type != "Холодное оружие":
        if defender.unit.unit_id == "3":
            damage -= defender.unit.rules["cut_enemy_damage"]
        elif armor in defender.inventory:
            damage -= armor.damage_reduction
    return damage