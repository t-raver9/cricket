from data_for_match import get_match_data
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
save_dir = os.path.dirname(dname) + r'/outputs/data/'
match_data_dir = save_dir + r'matches.csv'

# Create directory if it doesn't exist
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# Get match object for one of the matches
