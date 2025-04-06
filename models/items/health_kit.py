from models.items.item import Item


class HealthKit(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, hp):
        super().__init__(item_id, name, item_type, quantity, weight, info)
        self.hp = hp
        self.current_quantity = quantity

    def use(self):
        pass