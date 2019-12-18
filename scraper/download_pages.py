import os
import json
from download_urls import get_soup

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
match_dir = os.path.dirname(dname) + r'/outputs/matches/'

def match_urls_from_json():
    """
    Read in match URLs, which should be saved in JSON
    """
    read_path = os.path.dirname(dname) + r'/outputs' + r'/match_dict.json'
    with open(read_path,'r') as f:
        print("Reading in match URLs from JSON")
        match_dict = json.loads(f.read())
    return match_dict

def get_match_id(match_url: str) -> str:
    """
    Use the url of a match to deduce its match_id
    """
    match_id_start = match_url.find("/match/") + 7
    match_id_end = match_url.find(".html")
    match_id = match_url[match_id_start:match_id_end]
    return match_id

def check_already_downloaded(year: str, match_id: str) -> str:
    """
    Don't want to download any pages that we've already got. Use this function
    to return False if the page doesn't already exist in the save location.
    Else, return True.
    """
    save_path = match_dir + year + "/" + match_id + ".html"
    if os.path.exists(save_path):
        return True
    else:
        return False

def download_page(url: str, year: str, match_id: str):
    soup = get_soup(url)
    save_path = match_dir + year + "/" + match_id + ".html"
    with open(save_path,'w') as f:
        f.write(str(soup))
    print("Downloaded match_id {} from year {}".format(match_id, year))

def check_year_dir(year: str):
    if not os.path.exists(match_dir + year + r"/"):
        os.mkdir(match_dir + year + r"/")

def main():
    match_dict = match_urls_from_json()
    for year, match_list in match_dict.items():
        for match_url in match_list:
            match_id = get_match_id(match_url)
            check_year_dir(year)
            if not check_already_downloaded(year,match_id):
                download_page(match_url,year,match_id)
    print("All matches downloaded.")

if __name__ == "__main__":
    main()