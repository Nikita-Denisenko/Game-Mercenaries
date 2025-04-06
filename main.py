from game_management.current_game import CurrentGame
from game_management.entities import load_equipment, load_units, load_locations

equipment = load_equipment(r'D:\PyCharm projects\Game\data\equipment.json')
units = load_units(r'D:\PyCharm projects\Game\data\units.json')
locations = load_locations(r'D:\PyCharm projects\Game\data\locations.json', equipment)

players = None

current_game = CurrentGame(equipment, locations, units, players)