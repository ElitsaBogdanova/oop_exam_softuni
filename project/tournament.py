from project.equipment.elbow_pad import ElbowPad
from project.equipment.knee_pad import KneePad
from project.teams.indoor_team import IndoorTeam
from project.teams.outdoor_team import OutdoorTeam


class Tournament:
    EQUIPMENT_TYPES = {"ElbowPad": ElbowPad, "KneePad": KneePad}
    TEAM_TYPES = {"IndoorTeam": IndoorTeam, "OutdoorTeam": OutdoorTeam}

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.equipment = []
        self.teams = []
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value.isalnum():
            raise ValueError("Tournament name should contain letters and digits only!")
        self.__name = value

    def add_equipment(self, equipment_type):
        if equipment_type not in self.EQUIPMENT_TYPES:
            raise Exception("Invalid equipment type!")
        new_equipment = self.EQUIPMENT_TYPES[equipment_type]
        self.equipment.append(new_equipment)
        return f"{equipment_type} was successfully added."

    def add_team(self, team_type, team_name, country, advantage):
        if team_type not in self.TEAM_TYPES:
            raise Exception("Invalid team type!")

        if len(self.teams) == self.capacity:
            return "Not enough tournament capacity."

        new_team = self.TEAM_TYPES[team_type](team_name, country, advantage)
        self.teams.append(new_team)
        return f"{team_type} was successfully added."

    def sell_equipment(self, equipment_type, team_name):
        team = [t for t in self.teams if t.name == team_name][0]
        class_equipment = Tournament.EQUIPMENT_TYPES[equipment_type]
        equipment = [e for e in self.equipment if e.type_ == equipment_type][-1]

        if team.budget < equipment.price:
            raise Exception("Budget is not enough!")

        team.budget -= equipment.price
        team.equipment.append(equipment)
        self.equipment.remove(equipment)
        return f"Successfully sold {equipment_type} to {team_name}."

    def remove_team(self, team_name):
        team_exists = [t for t in self.teams if t.name == team_name]
        if not team_exists:
            raise Exception("No such team!")

        team = team_exists[0]
        if team.wins > 0:
            raise Exception(f"The team has {team.wins} wins! Removal is impossible!")

        self.teams.remove(team)
        return f"Successfully removed {team_name}."

    def increase_equipment_price(self, equipment_type):
        number_changed_prices = 0
        for e in self.equipment:
            if e.__class__.__name__ == equipment_type:
                e.increase_price()
                number_changed_prices += 1

        return f"Successfully changed {number_changed_prices}pcs of equipment."

    def play(self, team_name1, team_name2):
        first_team = [t for t in self.teams if t.name == team_name1][0]
        second_team = [t for t in self.teams if t.name == team_name2][0]

        if not first_team.__class__.__name__ == second_team.__class__.__name__:
            raise Exception("Game cannot start! Team types mismatch!")

        points_first_team = sum([e.protection for e in first_team.equipment]) + first_team.advantage
        points_second_team = sum([e.protection for e in second_team.equipment]) + second_team.advantage

        if points_first_team == points_second_team:
            return "No winner in this game."

        if points_first_team > points_second_team:
            first_team.win()
            return f"The winner is {first_team.name}."

        second_team.win()
        return f"The winner is {second_team.name}."

    def get_statistics(self):
        info = []
        info.append(f"Tournament: {self.name}")
        info.append(f"Number of Teams: {len(self.teams)}")
        info.append(f"Teams:")
        teams_sorted = sorted(self.teams, key = lambda x: x.wins, reverse=True)
        for team in teams_sorted:
            team_info = team.get_statistics()
            info.append(team_info)

        return "\n".join(info)


