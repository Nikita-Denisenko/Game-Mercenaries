from models.items.item import Item


class Armor(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, damage_reduction):
        super().__init__(item_id, name, item_type, quantity, weight, info)
        self.damage_reduction = damage_reduction
        self.current_quantity = quantity

    def use(self):
        pass