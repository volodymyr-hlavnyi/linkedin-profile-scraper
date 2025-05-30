import logging
import os
from os import environ as env

from dotenv import find_dotenv, load_dotenv

from logging import basicConfig, INFO

import gspread
from google.oauth2.service_account import Credentials

import validators

from chrome import (
    start_chrome_driver,
    stop_chrome_driver,
    go_to_linkedin_profile,
    get_name_from_linkedin_profile,
    get_location_from_linkedin_profile)

# Configure logging
basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Path to your service account file
SERVICE_ACCOUNT_FILE = env.get("GOOGLE_SERVICE_ACCOUNT_FILE", os.path.join(BASEDIR, "service_account.json"))
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
USERNAME = env.get("USERNAME", "your_username")
PROFILE_NAME = env.get("PROFILE_NAME", "your_profile_name")

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open your Google Sheet by URL
LINK_FILE_URL = env.get("GOOGLE_SHEET_URL")

scrapingbee_api_key = env.get('SCRAPINGBEE_API')

if __name__ == "__main__":

    sheet = client.open_by_url(LINK_FILE_URL)  # Replace with your Google Sheet URL
    worksheet = sheet.get_worksheet(0)  # First worksheet

    # Read the first column (assuming links are in column A)
    links = worksheet.col_values(1)

    logging.info("Found links:")
    valid_link = []
    for link in links:
        clear_link = link.strip()
        if validators.url(clear_link):
            # logging.info(f"Valid link: {link}")
            valid_link.append(link)
        else:
            logging.info(f"Invalid link: {clear_link}")

    next_step_2 = True

    if not next_step_2:
        logging.info("Next step 2 is not set, exiting.")
        exit(0)

    max_count_links = len(valid_link)
    current_link = 1

    driver = start_chrome_driver(USERNAME, PROFILE_NAME)

    for current_profile_url in valid_link:
        current_profile_url = current_profile_url.strip()

        logging.info(f"Processing link {current_link}: {current_profile_url}")

        go_to_linkedin_profile(driver, current_profile_url)
        full_name = get_name_from_linkedin_profile(driver)
        location = get_location_from_linkedin_profile(driver)

        links = worksheet.col_values(1)

        for idx, link in enumerate(links, start=1):
            if link.strip() == current_profile_url:
                worksheet.update_cell(idx, 2, full_name)  # Full Name in B
                worksheet.update_cell(idx, 3, location)  # Location in C
                logging.info(f"Wrote to row {idx}: {full_name}, {location}")
                break

        current_link += 1
        if current_link > max_count_links:
            break

    stop_chrome_driver(driver)
