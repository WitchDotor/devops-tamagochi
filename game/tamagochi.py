"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod
import random

from .models import Food, Medicine


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

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):

    def __init__(self, name: str, hunger: int, health: int, energy: int, mood: int):
        super().__init__()
        self.name = name
        self.hunger = hunger
        self.health = health
        self.energy = energy
        self.mood = mood

    def feed(self, food):
        """ """
        self.hunger+=food.satiety
        self.energy-=5
        self.mood-=5
        return super().feed(food)

    def play(self):
        """ """
        self.mood+=15
        self.energy-=5
        self.hunger-=5
        if random.randrange(0, 100, 1)>50:
            self.health-=random.randrange(0, 10, 1)
        return super().play()

    def rest(self):
        """ """
        self.hunger-=5
        self.mood-=5
        self.energy+=15
        return super().rest()

    def heal(self, medicine):
        """ """
        self.health+=medicine.heal_hp
        return super().heal(medicine)

    def status(self):
        super().status
        status = {
            'Health': self.health,
            'Hunger': self.hunger,
            'Energy': self.energy,
            'Mood': self.mood
        }
        return status

    def is_alive(self):
        super().is_alive()
        return self.health > 0

    def update(self):
        return super().update()