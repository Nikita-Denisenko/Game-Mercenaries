class Unit:
    def __init__(self, unit_id, units):
        self.unit_id = unit_id
        self.name = units[unit_id]["name"]
        self.max_health = units[unit_id]["health"]
        self.current_health = self.max_health
        self.actions = units[unit_id]["actions"]
        self.current_actions = self.actions
        self.weight = units[unit_id]["weight"]
        self.info = units[unit_id]["info"]
        self.rules = units[unit_id].get("rules", None)

    def take_damage(self, damage):
        self.current_health -= damage

    def restore_health(self, health_points):
        self.current_health = min(self.current_health + health_points, self.max_health)

    def use_actions(self, quantity_actions):
        if quantity_actions <= self.current_actions:
            self.current_actions -= quantity_actions
        else:
            print("Недостаточно действий! Ожидайте следующего хода.")

    def restore_actions(self):
        self.current_actions = self.actions

    def is_alive(self):
        return self.current_health > 0
