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


def print_the_map(locations, player):
    locations_info_dict = players_in_locations_info(locations, player)
    chemical_factory = locations_info_dict["Химический завод"]
    supermarket = locations_info_dict["Разгромленный супермаркет"]
    shore = locations_info_dict["Загрязнённое побережье"]
    wasteland = locations_info_dict["Пустошь"]
    eagle_cliff = locations_info_dict["Орлиный утёс"]
    train = locations_info_dict["Место крушения поезда"]
    hospital = locations_info_dict["Госпиталь"]

    print(f"                                      Карта                                  ")
    print(f"    {chemical_factory}                              {shore}             ")
    print("     ||====================||                        ||========================||")
    print("     ||  Химический завод  ||------------------------|| Загрязнённое побережье ||")
    print("     ||====================||                        ||========================||")
    print("      |                \                                     /             |   ")
    print("      |                  \                                 /               |   ")
    print(f"                                {wasteland}                                      ")
    print("      |                     \    ||===============||    /                  |   ")
    print("      |                       \  ||    Пустошь    ||  /                    |   ")
    print("      |                         \||===============||/                      |      ")
    print("      |                                   |                                |  ")
    print("      |                                   |                                |     ")
    print("      |                                   |                                |     ")
    print(f"      {train}                           {eagle_cliff}              {supermarket}           ")
    print("     ||=======================||       ||===============||         ||===========================||")
    print("     || Место крушения поезда ||-------|| Орлиный утёс] ||---------|| Разгромленный супермаркет ||")
    print("     ||=======================||       ||===============||         ||===========================||")
    print("                       \                                           /                              ")
    print("                        \                                       /                                 ")
    print("                         \                                   /                                    ")
    print("                          \                                /                                      ")
    print("                           \                            /                                         ")
    print("                            \                         /                                           ")
    print("                             ||===========||       /                                              ")
    print("                             || Госпиталь ||    /                                                 ")
    print("                             ||===========|| /                                                    ")
    print(f"                             {hospital}                                                          ")


def print_choose_action_text(location_explored, item_was_taken):
    print("Выберите действие:")
    print("1. Переместиться (1 или 2 действия)")
    if not location_explored:
        print("2. Обыскать локацию (1 действие)")
    else:
        if not item_was_taken:
            print("2. Взять предмет")
        else:
            print("2. Взять предмет (Недоступно)")
    print("3. Атаковать игрока (1 действие)")
    print("4. Вылечиться (1 действие)")
    print("5. Выбросить предмет из инвентаря")
    print("6. Завершить ход")


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

    names_string = input("Введите имена игроков через пробел: ")
    names = names_string.split()
    if len(names) != quantity:
        raise ValueError("Ошибка: Количество имен не совпадает с количеством игроков.")

    print("Игра успешно создана!")
    return quantity, names


def print_player_was_killed_text(player_name):
    print("-" * 60)
    print(f"Игрок {player_name} был убит от вашего выстрела!")
    print("-" * 60)
    print()


def print_player_was_damaged_text(player_name, damage, player):
    print("-" * 60)
    print(f"Игрок {player_name} получил {damage} урона от вашего выстрела.")
    print(f"Текущее здоровье игрока {player_name}: {player.unit.current_health} из {player.unit.max_health}")
    print("-" * 60)
    print()


def players_in_locations_info(locations, player):
    info_dict = {}
    for location in locations.values():
       current_players_names = [p.user_name for p in location.current_players if p != player]
       if location == player.location:
            current_players_names.append("(Вы здесь)!")
       current_players_info = ("Нет игроков", ", ".join(current_players_names))[len(current_players_names) > 0]
       info_dict[location.name] = current_players_info
    return info_dict


def next_to():
    input("Далее: ")