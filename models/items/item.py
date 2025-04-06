from abc import ABC


class Item(ABC):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.quantity = quantity
        self.weight = weight
        self.info = info
        self.rules = rules
