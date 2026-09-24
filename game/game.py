"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi, Tamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine


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

    def __init__(self, tamagochi: Tamagochi, clicker, all_food, all_medicine, money):
        super().__init__(tamagochi, clicker, all_food, all_medicine)
        self.tamagochi = tamagochi
        self.clicker = clicker
        self.all_food = all_food
        self.all_medicine = all_medicine
        self.money = money
        self.my_food = []
        self.my_medicine = []

    def work(self):
        """Clicker"""
        return super().work()

    def buy_food(self):
        food_number = f'Выберите еду: 1-{len(self.all_food)}'
        self.all_food.append(self.all_food[food_number-1])
        return super().buy_food()

    def buy_medicine(self):
        medicine_number = f'Выберите лекарство: 1-{len(self.all_medicine)}'
        self.my_medicine.append(self.all_medicine[medicine_number-1])
        return super().buy_medicine()

    def feed_tamagochi(self,):
        food_number = f'Выберите еду: 1-{len(self.my_food)}'
        self.tamagochi.feed(self.my_food[food_number-1])
        self.my_food.pop(food_number-1)
        return super().feed_tamagochi()

    def heal_tamagochi(self):
        medicine_number = f'Выберите лекарство: 1-{len(self.my_medicine)}'
        self.tamagochi.heal(self.my_medicine[medicine_number-1])
        return super().heal_tamagochi()

    def rest_tamagochi(self):
        self.tamagochi.rest()
        return super().rest_tamagochi()

    def play_with_tamagochi(self):
        self.tamagochi.play
        return super().play_with_tamagochi()

    def get_status(self):
        super().get_status()
        self.tamagochi.get_status
        return self.tamagochi.status()
    
    @property
    def food(self):
        return super().food

    @property
    def medicine(self):
        return super().medicine
