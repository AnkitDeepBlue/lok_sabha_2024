import json
import os
import re
import time
from centeral.helpers import WebScraperHelper
from centeral.locators import STATE_DROPDOWN_ID, CONSTITUENCY_DROPDOWN_ID, winner_candidate, looser_candidate,\
    complete_stats


def test_total_details(driver):
    url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
    driver.get(url)

    scraper = WebScraperHelper(driver)

    complete_state_table = scraper.wait_for_element(complete_stats).text

    # Parse the table and store the data in a dictionary
    data = {}
    majority_seats = 272

    lines = complete_state_table.split('\n')
    for line in lines:
        if line.startswith("Total"):
            continue  # Skip the total line
        match = re.match(r'(.+)\s-\s(\w+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
        if match:
            party_name = match.group(1).strip()
            party_abbr = match.group(2).strip()
            won = int(match.group(3).strip())
            leading = int(match.group(4).strip())
            total = int(match.group(5).strip())
            data[party_name] = {
                'party_abbr': party_abbr,
                'won': won,
                'leading': leading,
                'total': total
            }

    for party in data.values():
        party['sort_from_majority'] = majority_seats - party['total']

    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(project_root, 'data.json')

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)



