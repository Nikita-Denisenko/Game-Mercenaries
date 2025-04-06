from random import *

from models.items.armor import Armor
from models.items.artefact import Artefact
from models.items.camouflage import Camouflage
from models.items.health_kit import HealthKit
from models.items.weapon import Weapon
from models.items.weapon_upgrade import WeaponUpgrade


def choose_action_text():
    print("Выберите действие:")


def number_of_action_text():
    number = input("Введите номер действия: ")
    return number


def can_move_to_location(player, new_location_id):
    return new_location_id in player.location.adjacent_locations or new_location_id in player.location.distant_locations


def generate_item(location_items):
    number = randint(1, 100)
    for k, v in location_items.items():
        if number in range(v[0], v[1] + 1):
            return k


def spawn_item(location_items, items):
    item_id = generate_item(location_items)
    item_current_quantity = items[int(item_id) - 1].current_quantity
    while item_current_quantity == 0:
        item_id = generate_item(location_items)
        item_current_quantity = items[int(item_id) - 1].current_quantity
    return item_id


def create_item_from_data(item_id, item_data):

    item_type_to_class = {
        "Оружие": Weapon,
        "Бустер на оружие": WeaponUpgrade,
        "Броня": Armor,
        "Медикамент": HealthKit,
        "Артефакт": Artefact,
        "Маскировочное снаряжение": Camouflage
    }

    item_type_params = {
        "Медикаменты": ["hp"],
        "Оружие": ["weapon_type", "damage", "distance", "accuracy"],
        "Бустер на оружие": ["accuracy_bonus"],
        "Броня": ["damage_reduction"],
        "Маскировочное снаряжение": ["cut_enemy_accuracy"],
    }

    item_type = item_data.get("item_type")
    item_class = item_type_to_class.get(item_type)

    name = item_data.get("name")
    quantity = item_data.get("quantity")
    weight = item_data.get("weight")
    info = item_data.get("info")

    specific_params = {}
    for param_name in item_type_params.get(item_type, []):
        specific_params[param_name] = item_data.get(param_name)

    item = item_class(item_id, name, item_type, quantity, weight, info, **specific_params)

    return item
