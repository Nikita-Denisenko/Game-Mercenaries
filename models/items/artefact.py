from models.items.item import Item


class Artefact(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info, rules):
        super().__init__(item_id, name, item_type, quantity, weight, info, rules)
        self.current_quantity = quantity