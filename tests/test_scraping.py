import json
import os
import re
import time
from centeral.helpers import WebScraperHelper
from centeral.locators import STATE_DROPDOWN_ID, CONSTITUENCY_DROPDOWN_ID, winner_candidate, looser_candidate,\
    complete_stats

# constituencies.py
CONSTITUENCY_MAP = {
    "Agra": "Agra - 18",
    "Akbarpur": "Akbarpur - 44",
    "Aligarh": "Aligarh - 15",
    "Allahabad": "Allahabad - 52",
    "Ambedkar Nagar": "Ambedkar Nagar - 55",
    "Amethi": "Amethi - 37",
    "Amroha": "Amroha - 9",
    "Aonla": "Aonla - 24",
    "Azamgarh": "Azamgarh - 69",
    "Badaun": "Badaun - 23",
    "Baghpat": "Baghpat - 11",
    "Baharaich": "Baharaich - 56",
    "Ballia": "Ballia - 72",
    "Banda": "Banda - 48",
    "Bansgaon": "Bansgaon - 67",
    "Barabanki": "Barabanki - 53",
    "Bareilly": "Bareilly - 25",
    "Basti": "Basti - 61",
    "Bhadohi": "Bhadohi - 78",
    "Bijnor": "Bijnor - 4",
    "Bulandshahr": "Bulandshahr - 14",
    "Chandauli": "Chandauli - 76",
    "Deoria": "Deoria - 66",
    "Dhaurahra": "Dhaurahra - 29",
    "Domariyaganj": "Domariyaganj - 60",
    "Etah": "Etah - 22",
    "Etawah": "Etawah - 41",
    "Faizabad": "Faizabad - 54",
    "Farrukhabad": "Farrukhabad - 40",
    "Fatehpur": "Fatehpur - 49",
    "Fatehpur Sikri": "Fatehpur Sikri - 19",
    "Firozabad": "Firozabad - 20",
    "Gautam Buddha Nagar": "Gautam Buddha Nagar - 13",
    "Ghaziabad": "Ghaziabad - 12",
    "Ghazipur": "Ghazipur - 75",
    "Ghosi": "Ghosi - 70",
    "Gonda": "Gonda - 59",
    "Gorakhpur": "Gorakhpur - 64",
    "Hamirpur": "Hamirpur - 47",
    "Hardoi": "Hardoi - 31",
    "Hathras": "Hathras - 16",
    "Jalaun": "Jalaun - 45",
    "Jaunpur": "Jaunpur - 73",
    "Jhansi": "Jhansi - 46",
    "Kairana": "Kairana - 2",
    "Kaiserganj": "Kaiserganj - 57",
    "Kannauj": "Kannauj - 42",
    "Kanpur": "Kanpur - 43",
    "Kaushambi": "Kaushambi - 50",
    "Kheri": "Kheri - 28",
    "Kushi Nagar": "Kushi Nagar - 65",
    "Lalganj": "Lalganj - 68",
    "Lucknow": "Lucknow - 35",
    "Machhlishahr": "Machhlishahr - 74",
    "Maharajganj": "Maharajganj - 63",
    "Mainpuri": "Mainpuri - 21",
    "Mathura": "Mathura - 17",
    "Meerut": "Meerut - 10",
    "Mirzapur": "Mirzapur - 79",
    "Misrikh": "Misrikh - 32",
    "Mohanlalganj": "Mohanlalganj - 34",
    "Moradabad": "Moradabad - 6",
    "Muzaffarnagar": "Muzaffarnagar - 3",
    "Nagina": "Nagina - 5",
    "Phulpur": "Phulpur - 51",
    "Pilibhit": "Pilibhit - 26",
    "Pratapgarh": "Pratapgarh - 39",
    "Rae Bareli": "Rae Bareli - 36",
    "Rampur": "Rampur - 7",
    "Robertsganj": "Robertsganj - 80",
    "Saharanpur": "Saharanpur - 1",
    "Salempur": "Salempur - 71",
    "Sambhal": "Sambhal - 8",
    "Sant Kabir Nagar": "Sant Kabir Nagar - 62",
    "Shahjahanpur": "Shahjahanpur - 27",
    "Shrawasti": "Shrawasti - 58",
    "Sitapur": "Sitapur - 30",
    "Sultanpur": "Sultanpur - 38",
    "Unnao": "Unnao - 33",
    "Varanasi": "Varanasi - 77",
}

def parse_candidate_details(candidate_text):
    lines = candidate_text.split("\n")
    name = lines[2]
    total_votes = int(re.search(r"\d+", lines[1]).group())
    winning_margin = int(re.search(r"[+-]\s*(\d+)", lines[1]).group(1))
    party = lines[3].strip(", ")
    return {
        "Name": name,
        "Total Votes": total_votes,
        "Winning Margin": winning_margin,
        "Party": party
    }

def parse_candidate_details_looser(candidate_text):
    lines = candidate_text.split("\n")
    name = lines[2]
    total_votes = int(re.search(r"\d+", lines[1]).group())
    party = lines[3].strip(", ")
    return {
        "Name": name,
        "Total Votes": total_votes,
        "Party": party
    }

def test_scraping(driver, state_visible_text, constituency_name):
    url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
    driver.get(url)

    scraper = WebScraperHelper(driver)

    scraper.select_dropdown_option(STATE_DROPDOWN_ID, state_visible_text)

    constituency_value = CONSTITUENCY_MAP.get(constituency_name)
    if not constituency_value:
        constituency_value = constituency_name

    scraper.select_dropdown_option(CONSTITUENCY_DROPDOWN_ID, constituency_value)

    winner_text = scraper.wait_for_element(winner_candidate).text
    looser_text = scraper.wait_for_element(looser_candidate).text

    winner_details = parse_candidate_details(winner_text)
    looser_details = parse_candidate_details_looser(looser_text)

    # Save the details to a JSON file at the project level
    data = {
        "state": state_visible_text,
        "constituency": constituency_name,
        "winner": winner_details,
        "looser": looser_details
    }
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(project_root, 'candidate_data.json')

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

