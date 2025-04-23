class Player:
    def __init__(self, player_name, unit_id, start_location_id, units, locations, items):
        self.user_name = player_name
        self.unit = units[unit_id]
        self.items = items
        self.location = locations[start_location_id]
        self.inventory = []
        self.inventory_weight = 0
        self.different_artefacts = set()

    def take_item(self):
        action_cost = 1
        if self.unit.current_actions < action_cost:
            print("Недостаточно действий! Дождитесь следующего хода.")
            return
        item_id = self.location.location_item_id
        item = self.items[item_id]
        if self.inventory_weight + item.weight <= self.unit.weight:
            self.inventory.append(item)
            self.inventory_weight += item.weight
            item.current_quantity -= 1
            if item.item_type == "Артефакт":
                self.different_artefacts.add(item)
            self.unit.use_actions(action_cost)
        else:
            print("Вы не можете взять этот предмет!")

    def throw_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.inventory_weight -= item.weight
            item.current_quantity += 1
        else:
            print("У вас нет этого предмета в инвентаре!")

    def get_inventory_names(self):
        return [item.name for item in self.inventory]


    def change_location(self, new_location_id, locations):
        if new_location_id in self.location.adjacent_locations:
            action_cost = 1
        elif new_location_id in self.location.distant_locations:
            action_cost = 2
        else:
            print("Невозможно переместиться в эту локацию!")
            return

        if action_cost <= self.unit.current_actions:
            self.location.delete_player(self)
            self.location = locations[new_location_id]
            self.location.add_player(self)
            self.unit.use_actions(action_cost)
            print(f"{self.user_name} переместился в {self.location.name}")
        else:
            print("Недостаточно действий для перемещения! Дождитесь следующего хода.")


    def player_is_alive(self):
        return self.unit.is_alive()

