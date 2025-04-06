from models.items.item import Item


class Weapon(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules, weapon_type, damage, distance, accuracy):
        super().__init__(item_id, name, item_type, quantity, weight, info, rules)
        self.weapon_type = weapon_type
        self.damage = damage
        self.distance = distance
        self.accuracy = accuracy
        self.current_quantity = quantity