from utils.interface import print_choose_action_text, number_of_action, \
    print_player_was_killed_text, print_player_was_damaged_text, print_the_map, next_to
from utils.logic import calculate_distance, calculate_accuracy, calculate_damage, hit_the_player, \
    calculate_hand_fight_damage, is_crab_man, end_turn_for_player, is_grenade_launcher, \
    is_mp7, process_grenade_explosion, process_armor_break, process_second_shot_mp7, print_choose_the_location_info, \
    is_p350, two_pistols_logic, armor_is_broken, player_was_died_on_chemical_factory, lizard_man_logic, \
    is_chameleon_man, steal_item_for_chameleon_man, throw_item_from_inventory, check_one_survivor_flag

KNIFE = "4"
LASER_SIGHT = "10"
CAMOUFLAGE = "12"
ARMOR = "11"
HEALTH_KIT = "13"


class CurrentGame:
    def __init__(self, equipment, locations, units, players):
        self.equipment = equipment
        self.units = units
        self.locations = locations
        self.all_players = players
        self.alive_players = players
        self.day_number = 1
        self.game_is_over = False

    def finish_day(self):
        self.day_number += 1
        for player in self.alive_players:
            player.unit.restore_actions()
        print()
        print('*' * 60)
        print(f"День {self.day_number}")
        print('*' * 60)
        print()

    def kill_player(self, player):
        self.alive_players.remove(player)


    def print_players_info(self):
        players = self.alive_players
        for player in players:
            print(f"Имя: {player.user_name}; Персонаж: {player.unit.name};")
            print(f"Здоровье: {player.unit.current_health}; Локация: {player.location.name};")
            print("-" * 60)


    def choose_player_to_attack(self, attacker):
        players = [player for player in self.alive_players if player != attacker]
        print("Выберите игрока, которого хотите атаковать.")
        for i in range(1, len(players) + 1):
            player = players[i - 1]
            max_hp = player.unit.max_health
            hp = player.unit.current_health
            print(f"{i}. {player.user_name}({player.unit.name}) {hp} из {max_hp} жизней")
        number = None
        while number is None:
            number = number_of_action()
            if number is None or not (1 <= number <= len(players)):
                print("Некорректный номер игрока! Попробуйте снова.")
                number = None
        return players[number - 1]



    def print_locations_info(self):
        print("Информация о текущем местоположении игроков:")
        for location in self.locations:
            if location.current_players:
                players_names = ", ".join([player.user_name for player in location.current_players])
            else:
                players_names = "нет игроков"
            print(f"{location.name}: {players_names}")


    def weapon_fight(self, attacker, defender, weapon, laser_sight, camouflage, armor):
        if is_crab_man(attacker.unit):
            print()
            print("-" * 60)
            print("Вы не можете пользоваться оружием, у вас клешни! :)")
            print("-" * 60)
            return

        attackers_location = attacker.location
        defenders_location = defender.location
        distance = calculate_distance(attackers_location, defenders_location)
        accuracy = calculate_accuracy(attacker, defender, weapon, laser_sight, camouflage, distance)
        damage = calculate_damage(defender, weapon, armor)
        defender_name = defender.user_name

        if is_p350(weapon):
            if two_pistols_logic(self, attacker, defender, weapon, accuracy):
                return

        flag, number = hit_the_player(accuracy)

        if player_was_died_on_chemical_factory(self, attacker, attackers_location, number):
            return

        if not flag:
            if not is_mp7(weapon):
                print()
                print("-" * 60)
                print(f"Вы не попали в игрока {defender_name}!")
                print("-" * 60)
                return
            if not process_second_shot_mp7(self, attacker, defender, weapon, accuracy):
                return
        print()
        print("-" * 60)
        print(f"Вы попали в игрока {defender_name}!")

        if armor_is_broken(number):
            damage = process_armor_break(defender, damage, armor, camouflage)

        defender.unit.take_damage(damage)
        print_player_was_damaged_text(defender_name, damage, defender)

        if is_grenade_launcher(weapon):
            process_grenade_explosion(self, attacker, defender, weapon, defenders_location)

        if not defender.unit.is_alive():
            self.kill_player(defender)
            print_player_was_killed_text(defender_name)


    def hand_fight(self, attacker, defender, knife):
        defender_name = defender.user_name
        damage = calculate_hand_fight_damage(attacker, defender, knife)
        accuracy = knife.accuracy
        flag = hit_the_player(accuracy)[0]
        if not flag:
            print()
            print("-" * 60)
            print(f"Игрок {defender_name} увернулся от вашей атаки!")
            return
        print()
        print("-" * 60)
        print(f"Вы атаковали игрока {defender_name}!")

        defender.unit.take_damage(damage)

        if not defender.unit.is_alive():
            self.kill_player(defender)
            print(f"Игрок {defender_name} был убит от вашей атаки!")
            return

        print(f"Игрок {defender_name} получил {damage} урона от вашей атаки.")
        print(f"Текущее здоровье игрока {defender_name}: {defender.unit.current_health} из {defender.unit.max_health}")
        print("-" * 60)

    def attack_player(self, attacker):
        action_cost = 1
        equipment = self.equipment
        laser_sight = equipment[LASER_SIGHT]
        camouflage = equipment[CAMOUFLAGE]
        armor = equipment[ARMOR]
        knife = equipment[KNIFE]

        print_the_map(self.locations, attacker)
        print()

        defender = self.choose_player_to_attack(attacker)
        if defender is None:
            print("Цель не выбрана.")
            return

        distance = calculate_distance(attacker.location, defender.location)

        while True:
            print("Выберите тип атаки:")
            print("1. Стрельба из оружия")
            print("2. Рукопашная атака")
            print("3. Отменить")

            number = number_of_action()
            if number is None or number not in [1, 2, 3]:
                print("Неверный ввод, пожалуйста, выберите 1, 2 или 3.")
                continue

            if number == 3:
                print("Вы отменили атаку.")
                return

            if number == 1:
                weapon = attacker.choose_weapon()
                if weapon is None:
                    print("Оружие не выбрано.")
                    return

                if weapon.distance < distance:
                    print("Оружие не достаёт до цели.")
                    while True:
                        print("Хотите выбрать другую цель? (1 — да, 2 — нет)")
                        retry = number_of_action()
                        if retry in [1, 2]:
                            break
                        print("Неверный ввод. Введите 1 или 2.")

                    if retry == 1:
                        return  # Перезапуск атаки с новой целью
                    print("Вы отменили атаку.")
                    return

                self.weapon_fight(attacker, defender, weapon, laser_sight, camouflage, armor)
                attacker.unit.use_actions(action_cost)
                if check_one_survivor_flag(self.alive_players):
                    self.end_game()
                return

            if number == 2:
                if attacker.location != defender.location:
                    print("Рукопашная атака возможна только, если вы в одной локации с целью.")
                    while True:
                        print("Хотите выбрать другую цель? (1 — да, 2 — нет)")
                        retry = number_of_action()
                        if retry in [1, 2]:
                            break
                        print("Неверный ввод. Введите 1 или 2.")

                    if retry == 1:
                        return
                    print("Вы отменили атаку.")
                    return

                self.hand_fight(attacker, defender, knife)
                attacker.unit.use_actions(action_cost)
                if check_one_survivor_flag(self.alive_players):
                    self.end_game()
                return

    def heal_the_player(self, player):
        player.use_health_kit(self.equipment[HEALTH_KIT])
        player.unit.print_actions_info()


    def to_move_player(self, player):
        location = player.location
        locations = self.locations
        print_the_map(locations, player)
        print(f"Вы находитесь в локации {location.name}")
        print_choose_the_location_info(location, locations)
        while True:
            new_location_id = str(number_of_action())
            if new_location_id is None or not (1 <= int(new_location_id) <= len(locations)):
                print("Некорректный номер локации! Попробуйте снова.")
                continue
            player.change_location(new_location_id, locations)
            if player.location != location:
                break


    def search_location(self, player):
        action_cost = 1
        player.unit.use_actions(action_cost)
        location = player.location
        item_id = location.location_items_by_player.get(player.user_name)
        if item_id is None:
            print("В этой локации нет предметов.")
            return
        item = self.equipment[item_id]
        print(f"Вы нашли предмет: {item.name} (вес: {item.weight} кг).")
        print("Хотите взять его?")
        print("1. Да")
        print("2. Нет")
        choice = None
        while choice not in [1, 2]:
            choice = number_of_action()
            if choice is None:
                print("Некорректный ввод, попробуйте снова.")
        if choice == 1:
            player.take_item()
        else:
            print("Вы решили не брать предмет.")
        player.location_explored = True
        player.unit.print_actions_info()


    def spawn_start_items(self):
        for location in self.locations.values():
            for player in location.current_players:
                location.spawn_item_for_player(player)


    def player_turn(self, player):
        actions = {
            1: self.to_move_player,
            2: self.search_location,
            3: self.attack_player,
            4: self.heal_the_player,
            5: throw_item_from_inventory,
            6: end_turn_for_player,
            7: steal_item_for_chameleon_man
        }
        len_actions = len(actions) - 1 # Без действия хамелеона
        end_turn_for_player_number = 6
        while True:
            location_explored = player.location_explored
            item_was_taken = player.item_was_taken
            if location_explored:
                actions[2] = lambda p: p.take_item()
            print("-" * 60)
            print(f"Ходит игрок {player.user_name}")
            print("-" * 60)
            player.print_player_info()
            print("-" * 60)
            player.unit.print_unit_info()
            print("-" * 60)
            next_to()
            print("-" * 60)
            print_choose_action_text(location_explored, item_was_taken)
            if is_chameleon_man(player.unit):
                len_actions += 1 # Снимаем блокировку 7 ого действия, если игрок хамелеон
                print("7. Украсть предмет у игрока (1 действие)")
            print("-" * 60)
            while True:
                number = number_of_action()
                if number is None or not (1 <= number <= len_actions):
                    print("Некорректный номер действия. Попробуйте снова")
                    continue
                actions[number](player)
                if player.check_artefacts_flag():
                    self.end_game()
                next_to()
                break
            if player.unit.current_actions == 0:
                lizard_man_logic(player)
                print("У вас не осталось действий! Ход завершен!")
                actions[end_turn_for_player_number](player)
                next_to()
                return

    def end_game(self):
        self.game_is_over = True