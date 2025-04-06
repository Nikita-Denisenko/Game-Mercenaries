from models.items.item import Item


class HealthKit(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules, hp):
        super().__init__(item_id, name, item_type, quantity, weight, info, rules)
        self.hp = hp
        self.current_quantity = quantity

    def use(self, player):
        player.unit.restore_health(self.hp)