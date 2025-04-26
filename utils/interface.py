from utils.logic import calculate_change_location_cost


def print_hello_text():
    print('''
Добро пожаловать в игру Наёмники!
Игра представляет собой захватывающий многопользовательский экшен в жанре королевской битвы.
Здесь вы можете сражаться с другими игроками, используя разное оружие, поиграть за мутантов, 
появившихся из-за влияния радиации, исследовать локации, собирать артефакты и многое другое!
Используйте стратегическое мышление, а также всевозможные хитрости, чтобы собрать все три
магических артефакта, победить всех конкурентов, и конечно, выжить в этом жутком мире Пост-апокалипсиса!
''')


def print_the_rules_text():
    print('''
          Правила игры:
            
          '''
         )


def print_choose_action_text():
    print("Выберите действие:")
    print("1. Переместиться (1 или 2 действия)")
    print("2. Обыскать локацию (1 действие)")
    print("3. Атаковать игрока (1 действие)")
    print("4. Вылечиться (1 действие)")
    print("5. Завершить ход")


def number_of_action():
    try:
        number = int(input("Введите номер действия: "))
    except ValueError:
        print("Вы ввели некорректное значение")
        return None
    return number


def get_players_info():
    try:
        quantity = int(input("Введите количество игроков (от 2 до 6): "))
    except ValueError:
        raise ValueError("Ошибка: Пожалуйста, введите число от 2 до 6.")

    if not 2 <= quantity <= 6:
        raise ValueError("Ошибка: Количество игроков должно быть от 2 до 6.")

    names = input("Введите имена игроков через пробел: ").split()
    if len(names) != quantity:
        raise ValueError("Ошибка: Количество имен не совпадает с количеством игроков.")

    print("Игра успешно создана!")
    return quantity, names


def print_choose_the_location_info(player_location, locations):
    sorted_location_keys = sorted(locations.keys())
    for locations_id in sorted_location_keys:
        action_cost = calculate_change_location_cost(player_location, locations_id)
        location_name = locations[locations_id].name
        print(f"{locations_id}. {location_name} (Цена: {action_cost} действия)")