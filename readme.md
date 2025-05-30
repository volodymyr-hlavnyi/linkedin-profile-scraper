# LinkedIn Profile Info Scraper

A Python tool to automatically extract **Full Name** and **Location** from LinkedIn profiles listed in a Google Sheet, and write the results back to the same sheet.

---

## Features

- Reads LinkedIn profile links from a Google Sheets document
- Uses Selenium to visit each profile with your logged-in Chrome session
- Extracts Full Name and Location
- Writes the results back to your Google Sheet (next columns)
- Works with large lists and can be run headless on a server

---

## Installation

1. **Clone this repository:**
    ```bash
    git clone https://github.com/yourusername/linkedin-profile-scraper.git
    cd linkedin-profile-scraper
    ```

2. **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Setup Google Sheets API credentials:**
    - Create a Google Cloud service account and download the JSON key.
    - Share your Google Sheet with the service account email.
    - Save your JSON key as `service_account.json` in the project directory or set the path via `.env`.

4. **Prepare your `.env` file:**  
   Create a file named `.env` and set variables:
    ```
    GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
    GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit#gid=0
    USERNAME=your_linux_username
    PROFILE_NAME=Default  # Or your Chrome profile name
    ```

---

## Usage

1. **Login to LinkedIn in Chrome using your selected profile** (the script re-uses your cookies for scraping).

2. **Run the script:**
    ```bash
    python app.py
    ```

- The script will open Chrome, navigate to each LinkedIn profile from your sheet, extract data, and update the sheet.

---

## Requirements

- Python 3.8+
- Google Cloud Service Account (with Sheets access)
- A Google Sheet with LinkedIn profile URLs in column A

See `requirements.txt`:
