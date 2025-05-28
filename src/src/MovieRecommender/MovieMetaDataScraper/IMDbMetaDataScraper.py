import random

import pandas as pd
import variables
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

headers = variables.headers
filename = variables.filename


# Imports the necessary libraries for web scraping and data
def start_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values": {
            "cookies": 2,
            "images": 2,
            # "javascript": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--headless")
    options.add_argument("--disable-crash-reporter")

    user_agents: list[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    ]
    # Randomly select a User-Agent from the list
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    driver: webdriver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    print("Starting driver...")
    return driver


# Waits for an element to be present on the page
def wait_for_element(driver: webdriver) -> WebDriverWait:
    wait: WebDriverWait = WebDriverWait(driver, 10)

    return wait


# Creates CSV file for scraped metadata
def create_csv() -> None:
    print("Creating CSV file...")

    csv_file: pd.Dataframe = pd.DataFrame()
    csv_file.to_csv(filename, header=False, index=False, encoding="utf-8")

    print("Finished writing to CSV file.")

    return None


# Writes the scraped metadata to a CSV file
def write_to_csv(data_entry: pd.DataFrame) -> None:
    print("Adding entry to CSV file...")

    data_entry.to_csv(filename, header=False, mode="a", index=False)

    print("Added entry to CSV file.")

    return None


def total_movies(url: str) -> int:
    driver: webdriver = start_driver()
    driver.get(url)
    wait: WebDriverWait = wait_for_element(driver)

    results_location: str = variables.results_location

    wait.until(EC.presence_of_element_located((By.XPATH, results_location)))

    # Locate the element containing the total number of results
    results_element: WebElement = driver.find_element(By.XPATH, results_location)

    # Extract the number of results from the text
    number_movies: int = int(results_element.text.split(" ")[2].replace(",", ""))

    print("Total number of movies: ", number_movies)

    driver.quit()

    return number_movies


# Expands the page by clicking the "More" button until it is no longer present
def expand_page(driver: webdriver) -> None:
    print("Beginning to expand pages...")
    more_button_location = variables.more_button_location
    times_clicked: int = 0

    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    wait: WebDriverWait = wait_for_element(driver)

    click_more_element: WebElement = driver.find_element(By.XPATH, more_button_location)

    while True:
        try:
            driver.delete_all_cookies()
            # Wait for the "More" button to be present
            wait.until(EC.presence_of_element_located((By.XPATH, more_button_location)))

            click_more_element = driver.find_element(By.XPATH, more_button_location)

            # Scroll to the bottom of the page to load more results
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

            # Wait for the "More" button to be clickable
            wait.until(EC.element_to_be_clickable(click_more_element))

            # Click the "More" button
            driver.execute_script("arguments[0].click();", click_more_element)

            times_clicked += 1

            print(f"Clicked More, Page Expanded {times_clicked} times")

            # Wait for the "More" button to be removed from the DOM
            wait.until(EC.staleness_of(click_more_element))

        except NoSuchElementException:
            break

        except TimeoutException:
            break

    print("Reached End of Page.")

    return None


# Appends hyperlinks to a list
def grab_movie_links(driver: webdriver, number_movies: int) -> list[str]:
    block_location: str = variables.block_location
    link_location: str = variables.link_location
    # Finds all movie containers and number of them
    block_element: WebElement = driver.find_elements(By.CLASS_NAME, block_location)

    print("Grabbing Movie Links...")
    links_list: list[str] = []

    ######################### REMOVE THIS LATER: ########################
    number_movies = 1000

    for i in range(0, number_movies):
        grabbed_link: str = (
            block_element[i]
            .find_element(By.CLASS_NAME, link_location)
            .get_attribute("href")
        )
        links_list.append(grabbed_link)

    print("Finished grabbing movie links.")
    print(f"Grabbed {len(links_list)} movie links.")

    return links_list


# Grabs all movie links from the search results page
def find_number_of_movies_and_grab_all_links(url: str) -> list:
    number_movies: int = total_movies(url)

    driver: webdriver = start_driver()
    driver.get(url)

    expand_page(driver)

    links_list = grab_movie_links(driver, number_movies)

    driver.quit()

    return links_list


# Checks for the presence of an element on the page and returns its text
def check_for_element(
    driver: webdriver, selector_type: By, element_location: str, is_list: bool
) -> list[str] | str:
    if is_list:
        elements: list[str] = []
        try:
            temp_elements: list[WebElement] = driver.find_elements(
                selector_type, element_location
            )
            for element in temp_elements:
                elements.append(element.text)

            return elements

        except NoSuchElementException:
            elements = ["N/A"]
            return elements

    else:
        element: str = ""
        try:
            element = driver.find_element(selector_type, element_location).text
            return element

        except NoSuchElementException:
            element = "N/A"
            return element


def grab_meta_data(driver: webdriver, url: str) -> dict:
    # Movie Metadata HTML Constants
    title_location: str = variables.title_location
    year_location: str = variables.year_location
    parental_rating_location: str = variables.parental_rating_location
    runtime_location: str = variables.runtime_location
    rating_location: str = variables.rating_location
    languages_location: str = variables.languages_location
    genres_location: str = variables.genres_location
    directors_location: str = variables.directors_location
    actors_location: str = variables.actors_location
    description_url_location: str = variables.description_url_location
    description_location_1: str = variables.description_location_1
    description_location_2: str = variables.description_location_2

    print(f"Opening URL: {url}")
    driver.get(url)
    driver.set_window_size(720, 1280)

    wait_for_element(driver)
    print("Next Movie...")

    # Grabs movie title
    print("Grabbing title..")
    title: str = check_for_element(driver, By.CLASS_NAME, title_location, False)
    print(f"Title: {title}")

    # Grabs movie release year
    print("Grabbing Year..")
    year: str = check_for_element(driver, By.XPATH, year_location, False)
    print(f"Year: {year}")

    # Grabs movie parental rating
    print("Grabbing Parental Rating..")
    parental_rating: str = check_for_element(
        driver, By.XPATH, parental_rating_location, False
    )
    print(f"Parental Rating: {parental_rating}")

    # Grabs movie runtime
    print("Grabbing Runtime..")
    runtime: str = check_for_element(driver, By.XPATH, runtime_location, False)
    print(f"Runtime: {runtime}")

    # Grabs movie rating
    print("Grabbing Rating..")
    rating: str = check_for_element(driver, By.CLASS_NAME, rating_location, False)
    print(f"Rating: {rating}")

    # Grabs movie language
    print("Grabbing Language..")
    languages_temp: list[str] = check_for_element(
        driver, By.CSS_SELECTOR, languages_location, True
    )
    languages: str = ", ".join(languages_temp)
    print(f"Languages: {languages}")

    # Grabs movie genres
    print("Grabbing Genres..")
    genres_temp_1: list[str] = check_for_element(
        driver, By.XPATH, genres_location, True
    )
    genres_temp_2: list[str] = []
    for genre in genres_temp_1:
        genres_temp_2 = genre.split("\n")
    genres: str = ", ".join(genres_temp_2)
    print(f"Genres: {genres}")

    # Grabs movie director
    print("Grabbing Director..")
    directors_temp: list[str] = check_for_element(
        driver, By.XPATH, directors_location, True
    )
    directors: str = ", ".join(directors_temp)
    print(f"Directors: {directors}")

    # Grabs movie actors
    print("Grabbing Actors..")
    actors_temp: list[str] = check_for_element(driver, By.XPATH, actors_location, True)
    actors: str = ", ".join(actors_temp)
    print(f"Actors: {actors}")

    # Grabs movie description
    print("Grabbing Description..")
    description_see_more: str = check_for_element(
        driver, By.XPATH, description_url_location, False
    )

    if description_see_more == "Read all":
        description_url: str = driver.find_element(
            By.XPATH, description_url_location
        ).get_attribute("href")

        driver.get(description_url)
        wait_for_element(driver)

        description: str = check_for_element(
            driver, By.XPATH, description_location_1, False
        )
    else:
        description: str = check_for_element(
            driver, By.XPATH, description_location_2, False
        )

    print(f"Description: {description}")

    # Write data to CSV
    entry: dict = {
        "Title": title,
        "Year": year,
        "Parental Rating": parental_rating,
        "Runtime": runtime,
        "Rating": rating,
        "Language": languages,
        "Genres": genres,
        "Directors": directors,
        "Actors": actors,
        "Description": description,
        "URL": url,
    }

    return entry


def compile_meta_data(links_list: list[str]) -> None:
    # Iterates through each movie link and scrapes the metadata
    for url in links_list:
        driver: webdriver = start_driver()

        entry: dict = grab_meta_data(driver, url)

        print("Appending metadata entries to data frame...")
        print(entry)

        entry_data: pd.DataFrame() = pd.DataFrame(entry, index=[0])

        write_to_csv(entry_data)

        driver.quit()

    print("Finished appending metadata entries to list.")

    my_csv: pd.DataFrame = pd.DataFrame
    my_csv = pd.read_csv(filename)

    my_csv.columns = headers
    my_csv.to_csv(filename, header=headers, index=False)

    return None


def main() -> None:
    # Searches ImDB for movies released after 1920 with runtime greater than 60 minutes.
    my_url = variables.my_url

    create_csv()

    links_list: list[str] = find_number_of_movies_and_grab_all_links(my_url)
    compile_meta_data(links_list)

    return None


if __name__ == "__main__":
    main()
