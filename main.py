from game_management.current_game import CurrentGame
from utils.interface import print_hello_text, print_the_rules_text, get_players_info, next_to, print_the_map
from utils.loaders import load_equipment, load_units, load_locations, create_players

equipment = load_equipment(r'D:\PyCharm projects\Game\data\equipment.json')
units = load_units(r'D:\PyCharm projects\Game\data\units.json')
locations = load_locations(r'D:\PyCharm projects\Game\data\locations.json', equipment)

def main():
    print_hello_text()
    print_the_rules_text()

    # Получаем кортеж о количестве и именах игроков
    try:
        players_info = get_players_info()
    except ValueError as e:
        print(e)  # Выводим сообщение об ошибке
        return

    # Создаём игру
    quantity, names = players_info
    players = create_players(quantity, names, units, locations, equipment)
    game = CurrentGame(equipment, locations, units, players)
    next_to()

    game_loop(game)


def game_loop(game):
    game.spawn_start_items()
    print()
    print("Игра началась. Роли игроков следующие:")
    print("-" * 60)
    game.print_players_info()
    print("-" * 60)
    next_to()
    while True:
        for player in game.alive_players:
            print_the_map(game.locations, player)
            print("*" * 60)
            print(f"День {game.day_number}")
            print("*" * 60)
            game.player_turn(player)
            print()
            if game.game_is_over:
                return
        game.finish_day()
main()