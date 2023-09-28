from abc import ABC, abstractmethod
import math

class BaseTeam(ABC):
    def __init__(self, name, country, advantage, budget):
        self.name = name
        self.country = country
        self.advantage = advantage
        self.budget = budget
        self.wins = 0
        self.equipment = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value.strip() == '':
            raise ValueError("Team name cannot be empty!")
        self.__name = value
        
    @property
    def country(self):
        return self.__country
    
    @country.setter
    def country(self, value):
        if len(value.strip()) < 2:
            raise ValueError("Team country should be at least 2 symbols long!")
        self.__country = value
        
    @property
    def advantage(self):
        return self.__advantage
    
    @advantage.setter
    def advantage(self, value):
        if value <= 0:
            raise ValueError("Advantage must be greater than zero!")
        self.__advantage = value

    @abstractmethod
    def win(self):
        pass

    def get_statistics(self):
        equipment_price = sum(eq.price for eq in self.equipment)
        info = []
        info.append(f"Name: {self.name}")
        info.append(f"Country: {self.country}")
        info.append(f"Advantage: {self.advantage} points")
        info.append(f"Budget: {self.budget:.2f}EUR")
        info.append(f"Wins: {self.wins}")
        info.append(f"Total Equipment Price: {equipment_price:.2f}")
        info.append(f"Average Protection: {math.floor(equipment_price / len(self.equipment))}")

        return "\n".join(info)
