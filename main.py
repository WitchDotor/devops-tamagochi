import os

from game.clicker import TamagochiClicker
from game.constants import (BURGER,
                            SALAD,
                            APPLE,
                            IBUPROFEN,
                            HUNGER,
                            HEALTH,
                            ENERGY,
                            COINS,
                            MOOD)
from game.game import TamagochiGame
from game.models import Food, Medicine
from game.tamagochi import Tamagochi


def main():
    all_food = [
        Food(name=BURGER, satiety=20, price=40),
        Food(name=SALAD, satiety=10, price=20),
        Food(name=APPLE, satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name=IBUPROFEN, price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = Tamagochi(name='Олег',
                          hunger=50,
                          health=50,
                          energy=50,
                          mood=50)
    clicker = TamagochiClicker(click_reward=10)
    game = TamagochiGame(tamagochi=tamagochi,
                         clicker=clicker,
                         all_food=all_food,
                         all_medicine=all_medicine,
                         coins=0)

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()

        print(
            f"\nСтатус: голод: {status[HUNGER]}, "
            f"здоровье: {status[HEALTH]}, "
            f"энергия: {status[ENERGY]},"
            f"настроение: {status[MOOD]}, "
            f"монет: {status[COINS]}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        match input("Выберите действие: "):
            case "1":
                income = game.work()
                output = f'Вы заработали {income} монет'
                game.tamagochi.update()

            case "2":
                game.buy_food()

            case "3":
                game.buy_medicine()
            case "4":
                game.feed_tamagochi()

            case "5":
                game.heal_tamagochi()
            case "6":
                game.play_with_tamagochi()
                output = 'Вы поиграли с питомцем'
            case "7":
                game.rest_tamagochi()
                output = 'Питомец отдохнул'
            case "0":
                break
            case _:
                output = "Неверная команда"

        os.system('clear')


if __name__ == "__main__":
    main()
