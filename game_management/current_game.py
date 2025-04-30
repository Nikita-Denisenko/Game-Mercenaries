from utils.interface import print_choose_action_text, number_of_action, \
    print_player_was_killed_text, print_player_was_damaged_text, print_the_map
from utils.logic import calculate_distance, calculate_accuracy, calculate_damage, hit_the_player, \
    calculate_hand_fight_damage, is_crab_man, heal_the_player, end_turn_for_player, is_grenade_launcher, \
    is_mp7, process_grenade_explosion, process_armor_break, process_second_shot_mp7, print_choose_the_location_info

KNIFE = "4"
LASER_SIGHT = "10"
CAMOUFLAGE = "12"
ARMOR = "11"


class CurrentGame:
    def __init__(self, equipment, locations, units, players):
        self.equipment = equipment
        self.units = units
        self.locations = locations
        self.all_players = players
        self.alive_players = players
        self.day_number = 1

    def finish_day(self):
        self.day_number += 1
        for player in self.alive_players:
            player.unit.restore_actions()
        print(f"День {self.day_number}")


    def kill_player(self, player):
        self.alive_players.remove(player)


    def print_players_info(self):
        players = self.alive_players
        for player in players:
            print(f"Имя: {player.user_name}; Персонаж: {player.unit.name};")
            print(f"Здоровье: {player.unit.current_health}; Локация: {player.location.name};")
            print("-" * 30)


    def choose_player_to_attack(self):
        players = self.alive_players
        print("Выберите игрока, которого хотите атаковать.")
        for i in range(1, len(players) + 1):
            print(f"{i}. {players[i - 1].user_name}")
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
            print("Вы не можете пользоваться оружием, у вас клешни! :)")
            return

        attackers_location = attacker.location
        defenders_location = defender.location
        distance = calculate_distance(attackers_location, defenders_location)
        accuracy = calculate_accuracy(attacker, defender, weapon, laser_sight, camouflage, distance)
        damage = calculate_damage(defender, weapon, armor)
        defender_name = defender.name

        flag, number = hit_the_player(accuracy)

        if not flag:
            if not is_mp7(weapon):
                print(f"Вы не попали в игрока {defender_name}!")
                return
            if not process_second_shot_mp7(attacker, defender, weapon, damage, accuracy):
                return

        print(f"Вы попали в игрока {defender_name}!")

        if number == 6:
            damage = process_armor_break(defender, damage, armor, camouflage)

        defender.unit.take_damage(damage)
        print_player_was_damaged_text(defender_name, damage, defender)

        if is_grenade_launcher(weapon):
            process_grenade_explosion(self, attacker, defender, weapon, defenders_location)

        if not defender.unit.is_alive():
            self.kill_player(defender)
            print_player_was_killed_text(defender_name)

        attacker.unit.print_actions_info()


    def hand_fight(self, attacker, defender, knife):
        defender_name = defender.name
        damage = calculate_hand_fight_damage(attacker, defender, knife)
        accuracy = knife.accuracy
        flag = hit_the_player(accuracy)[0]
        if not flag:
            print(f"Игрок {defender_name} увернулся от вашей атаки!")
            return

        print(f"Вы атаковали игрока {defender_name}!")

        defender.unit.take_damage(damage)

        if not defender.unit.is_alive():
            self.kill_player(defender)
            print(f"Игрок {defender_name} был убит от вашей атаки!")
            return

        print(f"Игрок {defender_name} получил {damage} урона от вашей атаки.")
        print(f"Текущее здоровье игрока {defender_name}: {defender.unit.current_health} из {defender.unit.max_health}")
        attacker.unit.print_actions_info()


    def attack_player(self, attacker):
        action_cost = 1
        equipment = self.equipment
        laser_sight = equipment[LASER_SIGHT]
        camouflage = equipment[CAMOUFLAGE]
        armor = equipment[ARMOR]
        knife = equipment[KNIFE]

        while True:
            defender = self.choose_player_to_attack()
            if defender is None:
                print("Цель не выбрана.")
                return

            distance = calculate_distance(attacker.location, defender.location)

            print("Выберите тип атаки:")
            print("1. Стрельба из оружия")
            print("2. Рукопашная атака")
            print("3. Отменить")

            number = None
            while number not in [1, 2, 3]:
                number = number_of_action()

            if number == 3:
                print("Вы отменили атаку.")
                return

            if number == 1:
                weapon = attacker.choose_weapon()
                if weapon is None:
                    return
                if weapon.distance < distance:
                    print("Оружие не достаёт до цели.")
                    print("Хотите выбрать другую цель? (1 — да, 2 — нет)")
                    retry = number_of_action()
                    if retry == 1:
                        continue  # вернуться к выбору цели
                    else:
                        return

                self.weapon_fight(attacker, defender, weapon, laser_sight, camouflage, armor)
                attacker.unit.use_actions(action_cost)
                return

            elif number == 2:
                if attacker.location != defender.location:
                    print("Рукопашная атака возможна только, если вы в одной локации с целью.")
                    print("Хотите выбрать другую цель? (1 — да, 2 — нет)")
                    retry = number_of_action()
                    if retry == 1:
                        continue
                    else:
                        return

                self.hand_fight(attacker, defender, knife)
                attacker.unit.use_actions(action_cost)
                return


    def to_move_player(self, player):
        location = player.location
        locations = self.locations
        print_the_map()
        print(f"Вы находитесь в локации {location.name}")
        print_choose_the_location_info(location, locations)
        while True:
            new_location_id = number_of_action()
            if new_location_id is None or not (1 <= new_location_id <= len(locations)):
                print("Некорректный номер локации! Попробуйте снова.")
                continue
            player.change_location(new_location_id, locations)
            if player.location != location:
                break
        player.unit.print_actions_info()


    def search_location(self, player):
        action_cost = 1
        player.unit.use_actions(action_cost)
        location = player.location
        item_id = location.location_item_id
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
        if choice == 1:
            player.take_item()
            print(f"Вы подобрали предмет: {item.name} (вес: {item.weight} кг).")
        else:
            print("Вы решили не брать предмет.")
        player.unit.print_actions_info()


    def player_turn(self, player):
        actions = {
            1: self.to_move_player,
            2: self.search_location,
            3: self.attack_player,
            4: heal_the_player,
            5: end_turn_for_player,
        }
        end_turn_for_player_number = 5
        while True:
            print(f"Ходит игрок {player.user_name}")
            print("-" * 30)
            player.print_player_info()
            print("-" * 30)
            print_choose_action_text()
            print("-" * 30)
            while True:
                number = number_of_action()
                if number is None or not (1 <= number <= len(actions)):
                    print("Некорректный номер действия. Попробуйте снова")
                    continue
                actions[number](player)
                break
            if player.unit.current_actions == 0:
                print("У вас не осталось действий! Ход завершен!")
                actions[end_turn_for_player_number](player)
                return
