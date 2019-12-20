import urllib3
import os
from bs4 import BeautifulSoup as bs
import json
from typing import List, Dict, NoReturn

base_url = 'http://stats.espncricinfo.com'

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_soup(url: str) -> List:
    """
    Function to get the 'soup', i.e. the page contents, of any pages required
    """
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    soup = bs(response.data,features="lxml")
    return soup

def get_season_urls() -> List:
    """
    Function to get the URLs of every season test cricket has been played. Each
    of these URLs holds the matches played in that year
    """
    url = r'http://stats.espncricinfo.com/ci/content/records/307847.html'
    soup = get_soup(url)
    print("Getting URLs for each season")

    season_urls = []
    for link in soup.find_all('a'):
        if 'match_results' in link.get('href'):
            season_urls.append(link.get('href'))

    print("Season URLs downloaded")
    return season_urls

def get_match_urls(season_urls: List) -> Dict:
    """
    Get the URLs for each match. Input is the URLs which hold the
    matches for each season.
    """
    season_match_dict = {}

    for url in season_urls:
        # Extract the season to use as a key in the dictionary
        season_string_start = url.find('id=')+3
        season = url[season_string_start:season_string_start+4]
        season_match_dict[season] = []
        print("Downloading URLs from season {}".format(season))

        # For each season, get the URLs for the matches
        season_soup = get_soup(base_url + url)
        for link in season_soup.find_all('a'):
            href = link.get('href')
            if '/match/' in href:
                season_match_dict[season].append(base_url + href)

    return season_match_dict

def match_urls_to_json(season_match_dict: Dict) -> NoReturn:
    """
    Writes a dictionary of seasons, with the URLs of each match in that season,
    to a JSON
    """
    write_path = os.path.dirname(dname) + r'/outputs' + r'/match_dict.json'
    json_dict = json.dumps(season_match_dict)
    with open(write_path,'w') as f:
        f.write(json_dict)
    print("Match URLs saved as JSON")

def main():
    season_urls = get_season_urls()
    season_match_dict = get_match_urls(season_urls)
    match_urls_to_json(season_match_dict)

if __name__ == "__main__":
    main()
