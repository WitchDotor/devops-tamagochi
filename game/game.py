"""Модуль с интерфейсом и реализацией класса игры"""
import curses
import time
from abc import ABC, abstractmethod
from typing import Any
from game.clicker import AbstractClicker, TamagochiClicker
from game.constants import COINS
from game.models import Food, Medicine
from game.tamagochi import AbstractTamagochi, Tamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
            self,
            tamagochi: AbstractTamagochi,
            clicker: AbstractClicker,
            all_food: list[Food],
            all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class TamagochiGame(AbstractGame):

    def __init__(self, tamagochi: Tamagochi, clicker: TamagochiClicker, all_food, all_medicine, coins: int):
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.coins = coins
        self.my_food: list[Food] = []
        self.my_medicine: list[Medicine] = []

    def work(self):
        """Запускает кликер"""
        curses.wrapper(self.clicker.open_clicker)
        self.coins += self.clicker.income_in_session
        self.clicker.reset_income()

    def buy_food(self):
        """Покупка еды"""
        for i in self.all_food:
            index = self.all_food.index(i) + 1
            print(f'{index}. {i}')
        food_number = input(f'Выберите еду: 1-{len(self.all_food)}: ')
        index = int(food_number) - 1
        print(index)
        if not self.check_correct_input(index, self.my_medicine):
            return
        bought_food = self.all_food[index]
        if self.coins >= bought_food.price:
            self.my_food.append(bought_food)
            self.coins -= bought_food.price
        else:
            print('Не хватает денег')
            time.sleep(1)

    def buy_medicine(self):
        """Покупка медикоментов"""
        for i in self.all_medicine:
            index = self.all_medicine.index(i) + 1
            print(f'{index}. {i}')
        medicine_number = input(f'Выберите лекарство: 1-{len(self.all_medicine)}: ')
        index = int(medicine_number) - 1
        if not self.check_correct_input(index, self.my_medicine):
            return
        bought_medicine = self.all_medicine[index]
        if self.coins >= bought_medicine.price:
            self.my_medicine.append(bought_medicine)
            self.coins -= bought_medicine.price
        else:
            print('Не хватает денег')
            time.sleep(1)

    def feed_tamagochi(self):
        """Кормить тамагочи"""
        if len(self.my_food) == 0:
            print(f'У вас нет еды. Купите её!')
            return
        for i in self.my_food:
            index = self.my_food.index(i) + 1
            print(f'{index}. {i}')
        food_number = input(f'Выберите еду: 1-{len(self.my_food)}: ')
        index = int(food_number) - 1
        if not self.check_correct_input(index, self.my_medicine):
            return
        chosen_food = self.my_food[index]
        self.tamagochi.feed(chosen_food)
        self.my_food.pop(index)

    def heal_tamagochi(self):
        """Лечить тамагочи"""
        if len(self.my_medicine) == 0:
            print(f'У вас нет медикаментов Купите их!')
            time.sleep(1)
            return
        for i in self.my_medicine:
            index = self.my_medicine.index(i) + 1
            print(f'{index}. {i}')
        medicine_number = input(f'Выберите лекарство: 1-{len(self.my_medicine)}: ')
        index = int(medicine_number) - 1
        if not self.check_correct_input(index, self.my_medicine):
            return
        chosen_medicine = self.my_medicine[index]
        self.tamagochi.heal(chosen_medicine)
        chosen_medicine.number_of_uses = -1
        if chosen_medicine.number_of_uses == 0:
            self.my_medicine.pop(index)

    def rest_tamagochi(self):
        """Дать тамогочи отдохнуть"""
        self.tamagochi.rest()

    def play_with_tamagochi(self):
        """Играть с тамагочи"""
        self.tamagochi.play()

    def get_status(self):
        """Получить статус игры"""
        full_status = self.tamagochi.status
        full_status[COINS] = self.coins
        return full_status

    def check_correct_input(self, input: int, available_value: list) -> bool:
        """Проверить правильность ввода"""
        if input + 1 > len(available_value):
            return True
        else:
            print('Некоректный ввод')
            time.sleep(1)
            return False

    @property
    def food(self):
        """Геттер для имеющейся еды"""
        return self.my_food

    @property
    def medicine(self):
        """Геттер для имеющихся медикаментов"""
        return self.my_medicine
