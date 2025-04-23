from utils.interface import print_choose_action_text, number_of_action
from utils.logic import calculate_distance, calculate_accuracy, calculate_damage, hit_the_player, \
    calculate_hand_fight_damage, is_crab_man


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
                print("Некорректный номер игрока. Попробуйте снова.")
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
            print("Вы не можете пользоваться оружием, у вас клешни!:)")
            return
        attackers_location = attacker.location
        defenders_location = defender.location
        distance = calculate_distance(attackers_location, defenders_location)
        accuracy = calculate_accuracy(attacker, defender, weapon, laser_sight, camouflage, distance)
        damage = calculate_damage(defender, weapon, armor)
        defender_name = defender.name
        defender_inventory = defender.inventory
        flag, number = hit_the_player(accuracy)
        if not flag:
            print(f"Вы не попали в игрока {defender_name}!")
            return

        print(f"Вы попали в игрока {defender_name}!")

        if number == 6:
            if (armor in defender_inventory) or (camouflage in defender_inventory):
                defender.throw_item(armor)
                defender.throw_item(camouflage)
                damage += 20  # Разрушенный бронежилет не уменьшает урон от текущего выстрела
                print(f"Защитная экипировка игрока {defender_name} разрушена!")

        defender.unit.take_damage(damage)

        if not defender.unit.is_alive():
            self.kill_player(defender)
            print(f"Игрок {defender_name} был убит от вашего выстрела!")
            return

        print(f"Игрок {defender_name} получил {damage} урона от вашего выстрела.")
        print(f"Текущее здоровье игрока {defender_name}: {defender.unit.current_health} из {defender.unit.max_health}")
        return



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


    def attack_player(self, attacker):
        defender = self.choose_player_to_attack()
        print("Выберите тип атаки:")
        print("1. Стрельба из оружия")
        print("2. Рукопашная атака")
        number = None
        while number not in [1, 2]:
            number = number_of_action()
        equipment = self.equipment
        if number == 1:
            weapon = attacker.choose_weapon()
            if weapon is None:
                return
            laser_sight = equipment[LASER_SIGHT]
            camouflage = equipment[CAMOUFLAGE]
            armor = equipment[ARMOR]
            self.weapon_fight(attacker, defender, weapon, laser_sight, camouflage, armor)
        else:
            knife = equipment[KNIFE]
            self.hand_fight(attacker, defender, knife)


    def player_turn(self, player):
        actions = {

        }
        print(f"Ходит игрок {player.user_name}")
        print()
        player.print_player_info()
        print()
        print_choose_action_text()
        print()
