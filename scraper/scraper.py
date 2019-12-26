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

def get_page(url: str) -> list:
    """
    Function to get html contents of a webpage
    """
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    page = response.data.decode('utf-8')

    return page

def match_urls_from_json():
    """
    Read in match URLs, which should be saved in JSON
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

def check_page()

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