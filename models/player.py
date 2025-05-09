from utils.interface import number_of_action
from utils.logic import calculate_change_location_cost

WEAPON = "Оружие"
COLD_WEAPON = "Холодное оружие"

class Player:
    def __init__(self, player_name, unit_id, start_location_id, units, locations, items):
        self.user_name = player_name
        self.unit = units[unit_id]
        self.items = items
        self.location = locations[start_location_id]
        self.inventory = []
        self.inventory_weight = 0
        self.different_artefacts = set()
        self.location_explored = False
        self.item_was_taken = False


    def take_item(self):
        item_id = self.location.location_items_by_player.get(self.user_name)
        if item_id is None:
            print("В этой локации нет предметов для вас.")
            return
        item = self.items[item_id]
        if self.inventory_weight + item.weight > self.unit.weight:
            print("Вы не можете взять этот предмет!")
            return
        print(f"Вы подобрали предмет: {item.name} (вес: {item.weight} кг).")
        self.inventory.append(item)
        self.inventory_weight += item.weight
        item.current_quantity -= 1
        if item.item_type == "Артефакт":
            self.different_artefacts.add(item)
        self.item_was_taken = True
        del self.location.location_items_by_player[self.user_name]  # удалили после взятия


    def get_item(self, item):
        self.inventory.append(item)
        self.inventory_weight += item.weight
        item.current_quantity -= 1
        if item.item_type == "Артефакт":
            self.different_artefacts.add(item)


    def throw_item(self, item):
        if item not in self.inventory:
            print("У вас нет этого предмета в инвентаре!")
            return
        self.inventory.remove(item)
        self.inventory_weight -= item.weight
        item.current_quantity += 1
        if item.item_type == "Артефакт":
            self.different_artefacts.remove(item)


    def choose_the_item_to_throw(self):
        inventory_names = self.get_inventory_names()
        while True:
            print(f"Выберите предмет, который вы хотите выбросить из инвентаря:")
            for i in range(1, len(inventory_names) + 1):
                print(f"{i}. {inventory_names[i - 1]}")
            n = number_of_action()
            while n is None or not (1 <= n <= len(inventory_names)):
                print("Некорректный номер предмета! Попробуйте снова.")
                n = number_of_action()
            return n - 1  # возвращаем индекс, не id


    def get_inventory_names(self):
        return [item.name for item in self.inventory]


    def change_location(self, new_location_id, locations):
        action_cost = calculate_change_location_cost(self.location, new_location_id)
        if action_cost is None:
            print("Невозможно переместиться в эту локацию!")
            return

        if action_cost > self.unit.current_actions:
            print("Недостаточно действий для перемещения! Дождитесь следующего хода.")
            return

        self.location.delete_player(self)
        self.location = locations[new_location_id]
        self.location.add_player(self)
        self.location.spawn_item_for_player(self)
        self.unit.use_actions(action_cost)
        self.item_was_taken = False
        print(f"{self.user_name} переместился в {self.location.name}")


    def print_player_info(self):
        print(f"Игрок {self.user_name}")
        print(f"Персонаж: {self.unit.name}")
        print(f"Текущее здоровье: {self.unit.current_health} из {self.unit.max_health}")
        print(f"Количество действий: {self.unit.current_actions} из {self.unit.actions}")
        print(f"Локация: {self.location.name}")
        print("Предметы:")
        print(*self.get_inventory_names(), sep="\n")
        print(f"Вес инвентаря: {self.inventory_weight}кг.")


    def choose_weapon(self):
        predicate = lambda item: (item.item_type == WEAPON) and (item.weapon_type != COLD_WEAPON)
        weapons = list(filter(predicate, self.inventory))
        if len(weapons) == 0:
            print("У вас нет огнестрельного оружия в инвентаре!")
            return None
        print("Выберите оружие для стрельбы:")
        for i in range(1, len(weapons) + 1):
            print(f"{i}. {weapons[i - 1].name}")
        number = None
        while number is None:
            number = number_of_action()
            if number is None or not (1 <= number <= len(weapons)):
                print("Некорректный номер оружия. Попробуйте снова.")
                number = None
        return weapons[number - 1]

    def use_health_kit(self, health_kit):
        action_cost = 1
        if health_kit not in self.inventory:
            print("У вас нет аптечки в инвентаре!")
            return
        self.unit.restore_health(health_kit.hp)
        self.throw_item(health_kit)
        print(f"Вы использовали аптечку и восстановили {health_kit.hp} жизней.")
        self.unit.use_actions(action_cost)
        self.unit.print_actions_info()


    def end_turn(self):
        self.unit.current_actions = 0
        print(f"Игрок {self.user_name} завершил свой ход.")

    def check_artefacts_flag(self):
        return len(self.different_artefacts) == 3