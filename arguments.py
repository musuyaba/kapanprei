import argparse
from datetime import datetime

def get_year():
    parser = argparse.ArgumentParser(description='Fetch holiday data for a given year.')
    parser.add_argument('--year', type=int, help='The year for which to fetch the holiday data.')
    args = parser.parse_args()
    
    if args.year:
        return args.year
    else:
        return datetime.now().year