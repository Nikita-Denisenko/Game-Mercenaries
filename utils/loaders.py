import json

from models.location import Location
from models.player import Player
from models.unit import Unit
from utils.helpers import create_item_from_data
from random import shuffle, choice


def load_units(units_path):
    units = {}
    with open(units_path, 'r', encoding='UTF-8') as file:
        units_data = json.load(file)
    for i in units_data:
        units[i] = Unit(i, units_data)
    return units



def load_locations(locations_path, equipment):
    locations = {}
    with open(locations_path, 'r', encoding='UTF-8') as file:
        locations_data = json.load(file)
    for i in locations_data:
        locations[i] = Location(i, locations_data, equipment)
    return locations


def load_equipment(equipment_path):
    equipment = {}
    with open(equipment_path, 'r', encoding='UTF-8') as file:
        equipment_data = json.load(file)
    for i in equipment_data:
        equipment[i] = create_item_from_data(i, equipment_data[i])
    return equipment


def create_players(quantity, names, units, locations, items):
    players = {}
    units_id = units.keys()
    locations_id = locations.keys()
    shuffle(units_id)
    for i in range(quantity):
        player = Player(names[i], units_id[i], choice(locations_id), units, locations, items)
        players[str(i + 1)] = player
    return players
