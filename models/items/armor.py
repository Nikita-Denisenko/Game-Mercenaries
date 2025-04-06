from models.items.item import Item


class Armor(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules, damage_reduction):
        super().__init__(item_id, name, item_type, quantity, weight, info, rules)
        self.damage_reduction = damage_reduction
        self.current_quantity = quantity