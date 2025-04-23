from game_management.current_game import CurrentGame
from utils.interface import print_hello_text, print_the_rules_text, get_players_info
from utils.loaders import load_equipment, load_units, load_locations, create_players

equipment = load_equipment(r'D:\PyCharm projects\Game\data\equipment.json')
units = load_units(r'D:\PyCharm projects\Game\data\units.json')
locations = load_locations(r'D:\PyCharm projects\Game\data\locations.json', equipment)

game_over = False

def main():
    # Выводим текст приветствия
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

    game_loop(game)


def game_loop(game):
    while not game_over:
        for player in game.alive_players:
            print(f"День {game.day_number}")
            print(f"Ходит игрок {player.user_name}")
