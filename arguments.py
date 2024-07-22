import argparse
from datetime import datetime

def get_year():
    """
    Fetches the year for which to retrieve holiday data. If no year is provided as an argument,
    it defaults to the current year.

    Returns:
        int: The year for which to fetch the holiday data.
    """
    parser = argparse.ArgumentParser(description='Fetch holiday data for a given year.')
    parser.add_argument('--year', type=int, help='The year for which to fetch the holiday data.')
    args = parser.parse_args()
    
    if args.year:
        return args.year
    else:
        return datetime.now().year
