from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import typing

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
        self.batsmen = []
        self.bowlers = []
        self.scores = []

    def add_batsman(self,batsman):
        self.batsmen.append(batsman)

class Batsman:
    def __init__(self,name:str,position:int,how_out:str,runs:str,balls_faced:str,
    minutes:str,fours:str,sixes:str,strike_rate:str):
        self.name = name
        self.how_out = how_out
        self.runs = runs
        self.balls_faced = balls_faced
        self.minutes = minutes
        self.fours = fours
        self.sixes = sixes
        self.strike_rate = strike_rate

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

def get_batting_team(soup):
    for header in soup.findAll("div",{"class":"accordion-header"}):
        heading = header.find("a").text
        team = heading.split()[0]
    return team


path = "/Users/t_raver9/Desktop/projects/cricket/outputs/matches/1990/63534.html"
with open(path) as f:
    contents = f.read()

soup = bs(contents,features="lxml")

def get_batsman_data(soup):
    name = cell.find("div",{"class":"cell batsmen"}).text
    how_out = cell.find("div",{"class":"cell commentary"}).text
    runs = cell.find("div",{"class":"cell runs"}).text
    balls_faced = cell.find_all("div",{"class":"cell runs"})[1].text
    minutes = cell.find_all("div",{"class":"cell runs"})[2].text
    fours = cell.find_all("div",{"class":"cell runs"})[3].text
    sixes = cell.find_all("div",{"class":"cell runs"})[4].text
    strike_rate = cell.find_all("div",{"class":"cell runs"})[5].text

    return name,how_out,runs,balls_faced,minutes,fours,sixes,strike_rate

def get_bowler_data(tr):
    data = []
    for td in tr.find_all("td"):
            if (not td.attrs.get("class")):
                data.append(td.text)
    name,overs,maidens,runs,wickets,econ,wd,nb = [datum for datum in data]
    return name,overs,maidens,runs,wickets,econ,wd,nb 

# Create match object
match = Match()

# Find which teams are playing
teams = set()
for team in soup.findAll("span", {"class": "cscore_name cscore_name--long"}):
    teams.add(team.text)

# Get the scorecards of each innings
innings_soup_list = []
for innings_soup in soup.findAll("article", {"class": "sub-module scorecard"}):
    innings_soup_list.append(innings_soup)

# For each innings, find out who the team is and which innings it is
innings_ordered = OrderedDict()
innings_num = 1
for innings_soup in innings_soup_list:
    batting_team = innings_soup.find("div",{"class":"accordion-header"}).text.split()[0]
    inning = Innings(num=innings_num,batting_team=batting_team,teams=teams)
    match.add_innings(inning)
    
    # For each inning, get the details for each batsman
    batsman_cells = []
    for cell in soup.findAll("div", {"class": "wrap batsmen"}):
        batsman_cells.append(cell)
    
    position = 1
    for cell in batsman_cells:
        name,how_out,runs,balls_faced,minutes,fours,sixes,strike_rate = get_batsman_data(cell)
        batsman = Batsman(name,position,how_out,runs,balls_faced,minutes,fours,sixes,strike_rate)
        inning.add_batsman(batsman)
    

# Likewise, for each inning, get the details for each bowler
bowling_scorecard_objs = []
inning_idx = 0
for bowling_scorecard_obj in soup.findAll("div", {"class":"scorecard-section bowling"}):
    bowling_scorecard_objs.append(bowling_scorecard_obj)

    bowlers_tr = []
    position = 1
    for tr in bowling_scorecard_obj.find("tbody").find_all("tr"):
        bowlers_tr.append(tr)

        name,overs,maidens,runs,wickets,econ,wd,nb = get_bowler_data(tr)
        bowler = Bowler(name,position,overs,maidens,runs,wickets,econ,wd,nb)
        match.innings[inning_idx].bowlers.append(bowler)
        position += 1

    inning_idx += 1

print(match.innings[0].bowlers[0].name)
print(match.innings[0].bowlers[0].position)