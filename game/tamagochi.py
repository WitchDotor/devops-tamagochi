"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod
import random

from game.constants import HEALTH, HUNGER, ENERGY, MOOD
from game.models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

class Tamagochi(AbstractTamagochi):

    def __init__(self,
                 name: str,
                 hunger: int,
                 health: int,
                 energy: int,
                 mood: int):
        self.name = name
        self.hunger = hunger
        self.health = health
        self.max_health = health
        self.energy = energy
        self.mood = mood

    def feed(self, food):
        """Кормит питомца: восполняет голод за счёт сытости еды. """
        self.hunger += food.satiety
        self.energy -= 5
        self.mood -= 5

    def play(self):
        """Играет с питомцем: поднимает настроение, но утомляет."""
        self.mood += 15
        self.energy -= 5
        self.hunger -= 5
        if random.randrange(0, 100, 1) > 50:
            self.health -= random.randrange(0, 10, 1)

    def rest(self):
        """Отдых питомца: восстанавливает энергию."""
        self.hunger -= 5
        self.mood -= 5
        self.energy += 15

    def heal(self, medicine):
        """Лечит питомца с помощью лекарства."""
        self.health += medicine.heal_hp

    @property
    def status(self):
        """Возвращает словарь с текущими характеристиками питомца."""
        status = {
            HEALTH: self.health,
            HUNGER: self.hunger,
            ENERGY: self.energy,
            MOOD: self.mood
        }
        return status

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомецю"""
        return self.health <= self.max_health

    def is_alive(self):
        """Проверяет, жив ли питомец."""
        return self.health > 0