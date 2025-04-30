from random import choice

from utils.interface import print_player_was_killed_text, print_player_was_damaged_text, number_of_action

EAGLE_CLIFF = "7"
COLD_WEAPON = "Холодное оружие"
GUNFIGHTER = "4"
TORTOISE_MAN = "3"
HAND_FIGHTER = "2" # Бретер
CRAB_MAN = "8"
HAND_DAMAGE = 20
GRENADE_LAUNCHER = "8"
MP7 = "6"
P350 = "5"
GAME_CUBE_LIST = [1, 2, 3, 4, 5, 6]
GAME_CUBE_LIST_LENGTH = 6


def is_crab_man(unit):
    return unit.unit_id == CRAB_MAN

def is_grenade_launcher(weapon):
    return weapon.item_id == GRENADE_LAUNCHER

def is_mp7(weapon):
    return weapon.item_id == MP7

def is_p350(weapon):
    return weapon.item_id == P350


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


def print_choose_the_location_info(player_location, locations):
    sorted_location_keys = sorted(locations.keys())
    for locations_id in sorted_location_keys:
        action_cost = calculate_change_location_cost(player_location, locations_id)
        location_name = locations[locations_id].name
        print(f"{locations_id}. {location_name} (Цена: {action_cost} действия)")


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


def calculate_change_location_cost(location, new_location_id):
    if new_location_id in location.adjacent_locations:
        return 1
    if new_location_id in location.distant_locations:
        return 2
    return None


def heal_the_player(player):
    player.use_health_kit()
    player.unit.print_actions_info()

def end_turn_for_player(player):
    player.end_turn()


def get_adjacent_players(attacker, defender, defenders_location, locations):
    predicate = lambda player: player not in (attacker, defender)

    players_on_defenders_location = list(filter(predicate, defenders_location.current_players))
    adjacent_defenders_locations = [locations[l] for l in defenders_location.adjacent_locations]
    players_on_adjacent_defenders_locations = []

    for location in adjacent_defenders_locations:
        players = list(filter(predicate, location.current_players))
        players_on_adjacent_defenders_locations.extend(players)

    return players_on_defenders_location + players_on_adjacent_defenders_locations


def process_second_shot_mp7(attacker, defender, weapon, damage, accuracy):
    second_shot_accuracy = accuracy + weapon.rules["second_shot_cut_accuracy"]
    second_flag = hit_the_player(second_shot_accuracy)[0]

    defender_name = defender.name

    if not second_flag:
        print(f"Увы, вы не попали в игрока {defender_name} и со второго выстрела!")
        return False

    print(f"Вы попали в игрока {defender_name} со второго выстрела!")
    defender.unit.take_damage(damage)

    if not defender.unit.is_alive():
        attacker.game.kill_player(defender)
        print_player_was_killed_text(defender_name)

    print_player_was_damaged_text(defender_name, damage, defender)
    attacker.unit.print_actions_info()
    return True


def process_armor_break(defender, damage, armor, camouflage):
    defender_inventory = defender.inventory

    if (armor in defender_inventory) or (camouflage in defender_inventory):
        defender.throw_item(armor)
        defender.throw_item(camouflage)
        damage += 20
        print(f"Защитная экипировка игрока {defender.user_name} разрушена!")

    return damage


def process_grenade_explosion(game, attacker, defender, weapon, defenders_location):
    defenders_adjacent_players = get_adjacent_players(attacker, defender, defenders_location, game.locations)

    for player in defenders_adjacent_players:
        if player in (attacker, defender):
            continue
        player_name = player.user_name
        player_damage = weapon.rules["damage_for_adjacent_players"]

        player.unit.take_damage(player_damage)

        if not player.unit.is_alive():
            game.kill_player(player)
            print_player_was_killed_text(player_name)

        print_player_was_damaged_text(player_name, player_damage, player)


def two_pistols_logic(game, attacker, defender, weapon, damage, accuracy):
    if attacker.inventory.count(weapon) <= 1:
        return False

    print("Вы можете стрелять сразу из двух пистолетов, но с точностью -1 для обоих.")
    print("1. Использовать один пистолет")
    print("2. Использовать два пистолета")

    number = number_of_action()

    if number == 1:
        return False

    defender_name = defender.name

    for i in range(1, 3):
        print(f"Выстрел {i}")
        flag = hit_the_player(accuracy - weapon.rules["two_pistols_cut_accuracy"])[0]
        if not flag:
            print(f"Вы не попали в игрока {defender_name}!")
            continue
        defender.unit.take_damage(damage)
        print(f"Вы попали в игрока {defender_name}!")
        if not defender.unit.is_alive():
            game.kill_player(defender)
            print_player_was_killed_text(defender_name)
            return True
        print_player_was_damaged_text(defender_name, damage, defender)
    attacker.unit.print_actions_info()
    return True