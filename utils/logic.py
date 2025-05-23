from random import choice, randint

from utils.interface import print_player_was_killed_text, print_player_was_damaged_text, number_of_action, next_to

EAGLE_CLIFF = "7"
CHEMICAL_FACTORY = "4"
COLD_WEAPON = "Холодное оружие"
GUNFIGHTER = "4"
TORTOISE_MAN = "3"
HAND_FIGHTER = "2" # Бретер
CRAB_MAN = "8"
LIZARD_MAN = "5"
CHAMELEON_MAN = "6"
HAND_DAMAGE = 20
GRENADE_LAUNCHER = "8"
MP7 = "6"
P350 = "5"
ARMOR = "11"
GAME_CUBE_LIST = [1, 2, 3, 4, 5, 6]
GAME_CUBE_LIST_LENGTH = 6
BREAK_ARMOR_NUMBER = 6
INJURY_IN_CHEMICAL_FACTORY_NUMBER = 1


def is_crab_man(unit):
    return unit.unit_id == CRAB_MAN

def is_lizard_man(unit):
    return unit.unit_id == LIZARD_MAN

def is_chameleon_man(unit):
    return unit.unit_id == CHAMELEON_MAN


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


def generate_damage_from_range(damage_range):
    return randint(*damage_range)


def calculate_damage(defender, weapon, armor):
    damage = generate_damage_from_range(weapon.damage_range)
    if defender.unit.unit_id == TORTOISE_MAN:
        damage -= defender.unit.rules["cut_enemy_damage"]
    elif armor in defender.inventory:
        damage -= armor.damage_reduction
    return damage


def hit_the_player(accuracy):
    number = choice(GAME_CUBE_LIST)
    return number > (GAME_CUBE_LIST_LENGTH - accuracy), number


def print_choose_the_location_info(player_location, locations):
    sorted_location_keys = sorted(locations.keys(), key=int)
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
    else:
        damage += randint(*knife.rules["hand_damage_bonus_range"])

    if defender.unit.unit_id != TORTOISE_MAN:
        return damage
    return damage - defender.unit.rules["cut_enemy_damage"]


def calculate_change_location_cost(location, new_location_id):
    if new_location_id in location.adjacent_locations:
        return 1
    if new_location_id in location.distant_locations:
        return 2
    return None


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


def process_second_shot_mp7(game, attacker, defender, weapon, accuracy):
    damage = calculate_damage(defender, weapon, game.equipment[ARMOR])
    second_shot_accuracy = accuracy + weapon.rules["second_shot_cut_accuracy"]
    second_flag = hit_the_player(second_shot_accuracy)[0]

    defender_name = defender.name

    if not second_flag:
        print(f"Увы, вы не попали в игрока {defender_name} и со второго выстрела!")
        next_to()
        return False

    print(f"Вы попали в игрока {defender_name} со второго выстрела!")
    defender.unit.take_damage(damage)

    if not defender.unit.is_alive():
        game.kill_player(defender)
        print_player_was_killed_text(defender_name)
        next_to()

    print_player_was_damaged_text(defender_name, damage, defender)
    next_to()
    attacker.unit.print_actions_info()
    return True


def process_armor_break(defender, damage, armor, camouflage):
    defender_inventory = defender.inventory

    if (armor in defender_inventory) or (camouflage in defender_inventory):
        defender.throw_item(armor)
        defender.throw_item(camouflage)
        damage += 20
        print(f"Защитная экипировка игрока {defender.user_name} разрушена!")
        next_to()

    return damage


def armor_is_broken(number):
    return number == BREAK_ARMOR_NUMBER


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
            next_to()
            continue

        print_player_was_damaged_text(player_name, player_damage, player)
        next_to()


def two_pistols_logic(game, attacker, defender, weapon, accuracy):
    if attacker.inventory.count(weapon) <= 1:
        return False

    while True:
        print("1. Использовать один пистолет")
        print("2. Использовать два пистолета")
        number = number_of_action()
        if number in (1, 2):
            break
        print("Неверный ввод. Пожалуйста, введите 1 или 2.")

    if number == 1:
        return False

    defender_name = defender.name

    both_missed = True

    for i in range(1, 3):
        print(f"Выстрел {i}")
        flag, number = hit_the_player(accuracy - weapon.rules["two_pistols_cut_accuracy"])
        if not flag:
            print(f"Вы не попали в игрока {defender_name}!")
            next_to()
            continue
        both_missed = False
        damage = calculate_damage(defender, weapon, game.equipment[ARMOR])
        defender.unit.take_damage(damage)
        print(f"Вы попали в игрока {defender_name}!")
        if not defender.unit.is_alive():
            game.kill_player(defender)
            print_player_was_killed_text(defender_name)
            next_to()
            return True
        print_player_was_damaged_text(defender_name, damage, defender)
    player_was_died_on_chemical_factory(game, attacker, attacker.location, number)
    next_to()
    if both_missed:
        attacker.unit.print_actions_info()
        next_to()
    return True


def player_was_died_on_chemical_factory(game, attacker, attackers_location, number):
    if attackers_location.location_id != CHEMICAL_FACTORY:
        return False
    if number != INJURY_IN_CHEMICAL_FACTORY_NUMBER:
        return False
    damage = attackers_location.rules["missed_player_cut_health"]
    attacker.unit.take_damage(damage)
    if not attacker.unit.is_alive():
        game.kill_player(attacker)
        print("Вы умерли от травмы на химическом заводе!")
        next_to()
        return True
    print("Вы получили травму на химическом заводе и потеряли 20 жизней!")
    print(f"Ваше текущее здоровье: {attacker.unit.current_health} из {attacker.unit.max_health}")
    next_to()
    return False


def lizard_man_logic(player):
    if not is_lizard_man(player.unit):
        return
    hp_bonus = player.unit.rules["restore_hp_bonus"]
    player.unit.restore_health(hp_bonus)
    print(f'Вы использовали способность "Человека-ящера" и восстановили здоровье')
    print(f"Ваше текущее здоровье: {player.unit.current_health} из {player.unit.max_health}")
    next_to()


def choose_player_for_steal_item(chameleon, chameleon_player_location):
    players = [player for player in chameleon_player_location.current_players if player != chameleon]
    if len(players) == 0:
        print("В вашей локации нет игроков!")
        next_to()
        return None
    for i in range(1, len(players) + 1):
        player_name = players[i - 1].user_name
        print(f"{i}. {player_name}")
    print("Выберите игрока у которого вы хотите украсть предмет:")
    n = number_of_action()
    while n is None or not (1 <= n <= len(players)):
        print("Некорректный номер игрока! Попробуйте снова.")
        n = number_of_action()
    return players[n - 1]


def steal_item_for_chameleon_man(chameleon_player):
    action_cost = 1
    chameleon_player_location = chameleon_player.location
    while True:
        enemy = choose_player_for_steal_item(chameleon_player, chameleon_player_location)
        if enemy is None:
            return
        enemy_name = enemy.user_name
        enemy_inventory = enemy.inventory
        inventory_names = enemy.get_inventory_names()
        if len(enemy_inventory) == 0:
            print("У этого игрока нет предметов! Выберите другого.")
            next_to()
            continue
        print("1. Далее")
        print("2. Выбрать другого игрока")
        print("3. Отменить действие")
        n = number_of_action()
        while n is None or n not in (1, 2, 3):
            print("Некорректный номер предмета! Попробуйте снова.")
            n = number_of_action()
        if n == 3:
            print("Вы отменили действие.")
            next_to()
            return
        if n == 2:
            continue
        while True:
            print(f"Выберите предмет который вы хотите украсть у игрока {enemy_name}:")
            for i in range(1, len(inventory_names) + 1):
                print(f"{i}. {inventory_names[i - 1]}")
            n = number_of_action()
            while n is None or not (1 <= n <= len(inventory_names)):
                print("Некорректный номер предмета! Попробуйте снова.")
                n = number_of_action()
            item = enemy_inventory[n - 1]
            if chameleon_player.inventory_weight + item.weight > chameleon_player.unit.weight:
                print("В вашем инвентаре нет места для того, чтобы украсть этот предмет! Выберите другой.")
                print("1. Выбрать другой предмет")
                print("2. Выбрать другого игрока")
                print("3. Отменить действие")

                n = number_of_action()
                while n is None or n not in (1, 2, 3):
                    print("Некорректный номер предмета! Попробуйте снова.")
                    n = number_of_action()
                if n == 3:
                    print("Вы отменили действие.")
                    next_to()
                    return
                if n == 2:
                    break
                continue

            enemy.throw_item(item)
            chameleon_player.get_item(item)
            chameleon_player.unit.use_actions(action_cost)
            print(f'Вы украли предмет "{item.name}" у игрока {enemy_name}.')
            next_to()
            chameleon_player.unit.print_actions_info()
            next_to()
            return


def throw_item_from_inventory(player):
    item_index = player.choose_the_item_to_throw()
    item = player.inventory[item_index]
    player.throw_item(item)


def check_one_survivor_flag(alive_players):
    return len(alive_players) == 1
