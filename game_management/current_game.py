from utils.logic import calculate_distance, calculate_accuracy, calculate_damage, hit_the_player


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
        for player in self.alive_players.values():
            player.unit.restore_actions()
        print(f"День {self.day_number}")


    def kill_player(self, player):
        self.alive_players.remove(player)


    def print_players_info(self):
        for player_id, player in self.alive_players.items():
            print(f"Номер игрока: {player_id}; Имя: {player.user_name}; Персонаж: {player.unit.name};")
            print(f"Здоровье: {player.unit.current_health}; Локация: {player.location.name};")
            print()


    def weapon_fight(self, attacker, defender, weapon, laser_sight, camouflage, armor):
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



    def hand_fight(self, attacker, defender):
        pass
