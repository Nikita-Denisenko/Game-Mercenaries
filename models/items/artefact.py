from models.items.item import Item


class Artefact(Item):
    def __init__(self, item_id, name, item_type, quantity, weight, info):
        super().__init__(item_id, name, item_type, quantity, weight, info)
        self.current_quantity = quantity

    def use(self):
        pass