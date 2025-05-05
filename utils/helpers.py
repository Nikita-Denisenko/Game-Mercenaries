from random import *

from models.items.armor import Armor
from models.items.artefact import Artefact
from models.items.camouflage import Camouflage
from models.items.health_kit import HealthKit
from models.items.weapon import Weapon
from models.items.weapon_upgrade import WeaponUpgrade


def generate_item(location_items):
    number = randint(1, 100)
    for k, v in location_items.items():
        if number in range(v[0], v[1] + 1):
            return k


def create_item_from_data(item_id, item_data):
    name = item_data["name"]
    item_type = item_data["item_type"]
    quantity = item_data["quantity"]
    weight = item_data["weight"]
    info = item_data["info"]
    rules = item_data.get("rules", None)


    match item_type:
        case "Оружие":
            return Weapon(item_id, name, item_type, quantity, weight, info, rules,
                          item_data["weapon_type"], item_data["damage"],
                          item_data["distance"], item_data["accuracy"])

        case "Бустер на оружие":
            return WeaponUpgrade(item_id, name, item_type, quantity, weight, info, rules, item_data["accuracy_bonus"])

        case "Броня":
            return Armor(item_id, name, item_type, quantity, weight, info, rules, item_data["damage_reduction"])

        case "Медикамент":
            return HealthKit(item_id, name, item_type, quantity, weight, info, rules, item_data["hp"])

        case "Артефакт":
            return Artefact(item_id, name, item_type, quantity, weight, info, rules)

        case "Маскировочное снаряжение":
            return Camouflage(item_id, name, item_type, quantity, weight, info, rules, item_data["cut_enemy_accuracy"])
