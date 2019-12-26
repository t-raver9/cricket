from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from mapping_dict import mapping_dict
from classes import Match, Innings, Batsman, Bowler
import typing
import inspect

def get_teams_playing(soup):
    """
    Find which teams are playing the match
    """
    teams = set()
    for team in soup.findAll("span", {"class": "cscore_name cscore_name--long"}):
        teams.add(team.text)
    return teams

def get_innings_soup(soup):
    """
    Returns a list of HTML sections from the original soup. Each section is an
    'innings soup', a section of the HTML containing the data from one of the 
    innings
    """
    innings_soup_list = []
    for innings_soup in soup.findAll("article", {"class": "sub-module scorecard"}):
        innings_soup_list.append(innings_soup)
    return innings_soup_list

def get_batting_team(innings_soup):
    """
    Use innings soup to find which team is batting
    """
    batting_team = innings_soup.find("div",{"class":"accordion-header"}).\
        text.split()[0]
    return batting_team

def available_batsman_data(innings_soup,inning):
    """
    For each innings there is a row of html that defines what data is available
    for the batsman in that innings. This data isn't always the same, so it
    cannot be hardcoded. The function returns the available data, but also adds
    it to the inning objects for later processing
    """
    # First add the name and how out features, as these don't appear in the 
    # header we're using
    available_data = []
    available_data.extend(['Name','How Out'])
    inning.add_batsman_features(['Name','How Out'])
    # Loop through and pull out the data
    for header in innings_soup.find_all("div", {"class":"wrap header"}):
        for stat_header in header.find_all("div", {"class":"cell runs"}):
            available_data.extend(stat_header)
            inning.add_batsman_features(stat_header)
    return available_data

def get_batsman_soup(soup):
    """
    There's an area within each innings soup that has the batsman's scorecard. 
    This function retrieves each of these and returns them in a list.
    """
    batsman_soup_list = []
    for batsman_soup in soup.findAll("div", {"class": "wrap batsmen"}):
        batsman_soup_list.append(batsman_soup)
    return batsman_soup_list

def get_batsman_data(soup,batsman_features):
    """
    Given a row of HTML with batsman data for an innings, extract the data
    """
    data = []
    for div in soup.find_all("div"):
        if div['class'] != ["cell", "highlight" ,"active"]:
            data.append(div.text)
    #return dict(zip(batsman_features.keys(),data))
    return dict(zip(batsman_features,data))

def get_bowling_soup(soup):
    """
    Each bowling scorecard is contained in a section of HTML. This function
    returns a list containing each of those sections of HTML.
    """
    bowling_soup_list = []
    for bowling_soup in soup.findAll("div", {"class":"scorecard-section bowling"}):
        bowling_soup_list.append(bowling_soup)
    return bowling_soup


def get_bowler_data(tr):
    """
    Given a row of HTML with bowler data for an innings, extract the data
    """
    data = []
    for td in tr.find_all("td"):
            if (not td.attrs.get("class")):
                data.append(td.text)
    name,overs,maidens,runs,wickets,econ,wd,nb = [datum for datum in data]
    return name,overs,maidens,runs,wickets,econ,wd,nb 

def normalize_batsman_features(features):
    norm_features = []
    for feature in features:
        if feature in mapping_dict:
            norm_feature = mapping_dict[feature]
            norm_features.append(norm_feature)
        else:
            norm_features.append(feature)
    return norm_features

def get_match_data(match_path):
    # Read in the html contents
    #path = "/Users/t_raver9/Desktop/projects/cricket/outputs/matches/1990/63534.html"
    path = match_path
    with open(path) as f:
        contents = f.read()
    soup = bs(contents,features="lxml")

    # Create match object
    match = Match()

    # Find which teams are playing
    teams = get_teams_playing(soup)

    # Get the scorecard HTML of each innings
    innings_soup_list = get_innings_soup(soup)

    # Create an innings for each innings soup. 
    innings_num = 1
    for innings_soup in innings_soup_list:
        batting_team = get_batting_team(innings_soup)
        inning = Innings(num=innings_num,batting_team=batting_team,teams=teams)
        match.add_innings(inning)
        
        # Get HTML rows which have each batsman's data
        batsman_soup_list = get_batsman_soup(soup)

        # Retrieve the available batsman features
        batsman_features = available_batsman_data(innings_soup,inning)
        batsman_features = normalize_batsman_features(batsman_features)
        
        # For each batsman, pull out the available data and create a batsman object
        position = 1
        for batsman_soup in batsman_soup_list:
            batsman_data = get_batsman_data(batsman_soup,batsman_features)
            batsman = Batsman(**batsman_data)
            inning.add_batsman(batsman)
        
    # Likewise, for each inning, get the details for each bowler
    inning_idx = 0
    bowling_soup_list = get_bowling_soup(soup)

    for bowling_soup in bowling_soup_list:
        bowlers_tr = []
        position = 1
        for tr in bowling_soup.find("tbody").find_all("tr"):
            bowlers_tr.append(tr)
            name,overs,maidens,runs,wickets,econ,wd,nb = get_bowler_data(tr)
            bowler = Bowler(name,position,overs,maidens,runs,wickets,econ,wd,nb)
            match.innings[inning_idx].bowlers.append(bowler)
            position += 1

        inning_idx += 1

    # Get totals
    innings_idx = 0
    for total_soup in soup.find_all("div", {"class":"wrap total"}):
        for div in total_soup.find_all("div"):
            if div.text != "TOTAL":
                match.innings[innings_idx].total = div.text.split()[0].split("/")[0]
                print(match.innings[innings_idx].total)
        innings_idx += 1

    # Return match object
    return match