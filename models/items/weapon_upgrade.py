from models.items.item import Item


class WeaponUpgrade(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, accuracy_bonus):
        super().__init__(item_id, name, item_type, quantity, weight, info)
        self.accuracy_bonus = accuracy_bonus
        self.current_quantity = quantity

    def use(self):
        pass