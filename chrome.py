from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def start_chrome_driver(username, profile_name):
    chrome_options = Options()
    # Use your real path!
    chrome_options.add_argument(f"user-data-dir=/home/{username}/.config/google-chrome")
    # chrome_options.add_argument("profile-directory=Default")  # Most people use Default
    chrome_options.add_argument(f"profile-directory={profile_name}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Go to LinkedIn (should be logged in automatically)
    driver.get("https://www.linkedin.com/")
    time.sleep(10)  # Wait for page to load and for you to see the window

    return driver


def stop_chrome_driver(driver):
    try:
        time.sleep(10)
        driver.quit()
    except Exception as e:
        print("Error stopping Chrome driver:", e)


def go_to_linkedin_profile(driver, profile_url):
    try:
        driver.get(profile_url)
        time.sleep(6)  # Wait for the page to load
    except Exception as e:
        print("Error navigating to LinkedIn profile:", e)


def get_name_from_linkedin_profile(driver):
    try:
        # The name is usually inside a <h1> tag on the profile page
        name_elem = driver.find_element(By.TAG_NAME, "h1")
        full_name = name_elem.text.strip()
        return full_name
    except Exception as e:
        print("Could not extract name:", e)
        return ''


def get_location_from_linkedin_profile(driver):
    try:
        # Find all spans with the correct class
        location_elems = driver.find_elements(By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light.break-words")
        # Get the first one with non-empty text
        location = ""
        for elem in location_elems:
            txt = elem.text.strip()
            if txt:
                location = txt
                break
        return location
    except Exception as e:
        print("Could not extract location:", e)
        return ''
