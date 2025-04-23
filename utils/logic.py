from random import choice

EAGLE_CLIFF = "7"
COLD_WEAPON = "Холодное оружие"
GUNFIGHTER = "4"
TORTOISE_MAN = "3"
HAND_FIGHTER = "2" # Бретер
CRAB_MAN = "8"
HAND_DAMAGE = 20

GAME_CUBE_LIST = [1, 2, 3, 4, 5, 6]
GAME_CUBE_LIST_LENGTH = 6

def is_crab_man(unit):
    return unit.unit_id == CRAB_MAN

def calculate_distance(attackers_location, defenders_location):
    if attackers_location == defenders_location:
        return 0

    distance = 0

    if attackers_location.location_id == EAGLE_CLIFF:
        distance -= attackers_location.rules["cut_distance_bonus"]

    defenders_id = defenders_location.location_id

    if defenders_id in attackers_location.unavailable_locations:
        return distance + 3
    if defenders_id in attackers_location.distant_locations:
        return distance + 2
    return distance + 1



def calculate_accuracy(attacker, defender, weapon, laser_sight, camouflage, distance):
    accuracy = weapon.accuracy
    accuracy -= distance
    if weapon.weapon_type != COLD_WEAPON:
        if attacker.unit.unit_id == GUNFIGHTER:
            accuracy += attacker.unit.rules["accuracy_bonus"]
        if laser_sight in attacker.inventory:
            accuracy += laser_sight.rules["accuracy_bonus"]
    if defender.unit.unit_id == TORTOISE_MAN:
        accuracy -= defender.unit.rules["cut_enemy_accuracy"]
    elif camouflage in defender.inventory:
        accuracy -= camouflage.rules["cut_enemy_accuracy"]
    return accuracy


def calculate_damage(defender, weapon, armor):
    damage = weapon.damage
    if weapon.weapon_type != COLD_WEAPON:
        if defender.unit.unit_id == TORTOISE_MAN:
            damage -= defender.unit.rules["cut_enemy_damage"]
        elif armor in defender.inventory:
            damage -= armor.damage_reduction
    return damage


def hit_the_player(accuracy):
    number = choice(GAME_CUBE_LIST)
    return number > (GAME_CUBE_LIST_LENGTH - accuracy), number


def calculate_hand_fight_damage(attacker, defender, knife):
    if is_crab_man(attacker.unit):
        return attacker.unit.rules["damage"]
    damage = HAND_DAMAGE
    if knife not in attacker.inventory:
        if attacker.unit.unit_id != HAND_FIGHTER:
            return damage
        damage += attacker.unit.rules["hand_attack_bonus"]
    damage += knife.rules["hand_damage_bonus"]

    if defender.unit.unit_id != TORTOISE_MAN:
        return damage
    return damage - defender.unit.rules["cut_enemy_damage"]
