from models.items.item import Item


class Camouflage(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules, cut_enemy_accuracy):
        super().__init__(item_id, name, item_type, quantity, weight, info, rules)
        self.cut_enemy_accuracy = cut_enemy_accuracy
        self.current_quantity = quantity