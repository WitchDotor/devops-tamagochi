"""Модуль с интерфейсом и реализацией кликера"""
import curses
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class TamagochiClicker(AbstractClicker):
    def __init__(self, click_reward: int):
        self.click_reward = click_reward
        self.income_in_session = 0
        self.stdscr = None

    @property
    def income_per_click(self):
        """Геттер для текущего заработка за клик"""
        return self.click_reward

    def open_clicker(self, stdscr):
        """Запускает окно кликера"""
        self.stdscr = stdscr
        curses.mousemask(curses.BUTTON1_CLICKED | curses.BUTTON1_RELEASED)

        self.stdscr.addstr(0, 0, "Клик — кормить, q — выход")
        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_MOUSE:
                try:
                    _, mx, my, _, bstate = curses.getmouse()
                except curses.error:
                    continue

                if bstate & (curses.BUTTON1_CLICKED | curses.BUTTON1_RELEASED):
                    self.click()
                    message = (f"Клик — кормить, q — выход \n"
                               f"Заработано: {self.income_per_click}, "
                               f"всего: {self.income_in_session}")
                    self.stdscr.clear()
                    self.stdscr.addstr(0, 0, message)
                    self.stdscr.refresh()

            elif key == ord('q'):
                self.stdscr.clear()
                self.stdscr.refresh()

                break

    def click(self):
        """Увеличивает текущий запас монет"""
        self.income_in_session += self.income_per_click

    def reset_income(self):
        """Сбрасывает счет монет за сессию"""
        self.income_in_session = 0
