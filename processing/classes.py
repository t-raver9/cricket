from collections import OrderedDict

class Match:
    def __init__(self):
        self.innings = []

    def add_innings(self,inning):
        self.innings.append(inning)

class Innings:
    def __init__(self, num:int,batting_team: str, teams:set):
        self.num = num
        self.teams = teams
        self.batting_team = batting_team
        self.bowling_team = list(teams - {batting_team})[0]
        self.total = None
        self.batsmen = []
        self.bowlers = []
        self.scores = []
        self.batsman_features = []
        self.fow = OrderedDict()

    def add_batsman(self,batsman):
        self.batsmen.append(batsman)

    def add_batsman_features(self,features):
        self.batsman_features.extend(features)

class Batsman:
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Bowler:
    def __init__(self,name:str,position:int,overs:str,maidens:str,runs:str,
    wickets:str,econ:str,wd:str,nb:str):
        self.name = name
        self.position = position
        self.overs = overs
        self.maidens = maidens
        self.runs = runs
        self.wickets = wickets
        self.econ = econ
        self.wd = wd
        self.nb = nb