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


    def kill_player(self, player_id):
        self.alive_players.pop(player_id)


    def print_players_info(self):
        for player_id, player in self.alive_players.items():
            print(f"Номер игрока: {player_id}; Имя: {player.user_name}; Персонаж: {player.unit.name};")
            print(f"Здоровье: {player.unit.current_health}; Локация: {player.location.name};")
            print()


    def weapon_fight(self, attacker, defender, weapon):
        pass


    def hand_fight(self, attacker, defender):
        pass
