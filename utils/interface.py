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


def print_the_map():
    print(                                "Карта"                                 )
    print(                                                                        )
    print("      [Химический завод]----------------------[Загрязнённое побережье]")
    print("      |                 \                    /                 |      ")
    print("      |                  \                  /                  |      ")
    print("      |                   \                /                   |      ")
    print("      |                    \              /                    |      ")
    print("      |                     \            /                     |      ")
    print("      |                      \          /                      |      ")
    print("      |                       [Пустошь]                        |      ")
    print("      |                           |                            |      ")
    print("      |                           |                            |      ")
    print("      |                           |                            |      ")
    print("      |                           |                            |      ")
    print("[Место крушения поезда]-----[Орлиный утёс]-----[Разгромленный супермаркет]")
    print("                      \                       /                           ")
    print("                       \                     /                            ")
    print("                        \                   /                             ")
    print("                         \                 /                              ")
    print("                          \               /                               ")
    print("                           \             /                                ")
    print("                             [Госпиталь]                                  ")


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

print_the_map()