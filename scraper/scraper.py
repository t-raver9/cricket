import urllib3
import os
from bs4 import BeautifulSoup as bs
import json
from typing import List

base_url = 'http://stats.espncricinfo.com'

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Functions

def get_soup(url: str) -> list:
    """
    Function to get the 'soup', i.e. the page contents, of any pages required
    """
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    soup = bs(response.data,features="lxml")

    return soup

def get_page(url: str) -> list:
    """
    Function to get html contents of a webpage
    """
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    page = response.data.decode('utf-8')

    return page


def get_season_urls() -> list:
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


def get_match_urls(season_urls: list) -> dict:
    """
    Function to get the URLs for each match. Input is the URLs which hold the
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

def match_urls_to_json(season_match_dict: dict):
    """
    Writes a dictionary of seasons, with the URLs of each match in that season,
    to a JSON
    """
    write_path = os.path.dirname(dname) + r'/outputs' + r'/match_dict.json'
    json_dict = json.dumps(season_match_dict)
    with open(write_path,'w') as f:
        f.write(json_dict)
    print("Match URLs saved as JSON")

def match_urls_from_json():
    """
    Read in the URLs previously saved in json format
    """
    read_path = os.path.dirname(dname) + r'/outputs' + r'/match_dict.json'
    with open(read_path,'r') as f:
        print("Reading in match URLs from JSON")
        match_dict = json.loads(f.read())
    return match_dict

def get_match_id_from_url(match_url: str) -> str:
    match_id_start = match_url.find("/match/") + 7
    match_id_end = match_url.find(".html") - 1
    match_id = match_url[match_id_start:match_id_end]
    return match_id

#def save_page()

#def download_match_pages(match_dict: dict):
#    for year, match_url in match_dict.items():
#        match_id = get_match_id_from_url(match_url)
#        save_path = 



def main():
    # Get URLs for seasons.
    season_urls = get_season_urls()

    # Get the match URLs for each game. 
    season_match_dict = get_match_urls(season_urls)
    match_urls_to_json(season_match_dict)

    # If you've already got the match URLs, just read them in from the json file they're housed
    # in and continue
    season_match_dict = match_urls_from_json()
    print(season_match_dict)

    # Try to get the relevant data from each URL without needing to download a page.
    #test_url = season_match_dict['2014'][0]
    #soup = get_soup(test_url)

    # Download pages if they don't exist
    
    

if __name__ == "__main__":
    main()