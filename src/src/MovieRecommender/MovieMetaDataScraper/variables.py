results_location: str = '//div[contains(text(), "1-50 of ")]'
more_button_location = "//div[@id='__next']/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span"
block_location: str = "ipc-metadata-list-summary-item"
link_location: str = "ipc-title-link-wrapper"
title_location: str = "hero__primary-text"
year_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a'
parental_rating_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a'
runtime_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]'
rating_location: str = "ipc-rating-star--rating"
languages_location: str = 'a[href*="language"]'
genres_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]'
directors_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/ul/li[1]/div'
actors_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[2]/ul/li[3]/div'
description_url_location: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[1]/a'
description_location_1: str = '//*[@id="py8555146"]/div/div/div/div/div'
description_location_2: str = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[1]'

my_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1920-01-01,&runtime=60,"
"""my_url = (
    "https://www.imdb.com/search/title/?title_type=feature&genres=action&runtime=45,45"
)"""

headers = [
    "Title",
    "Year",
    "Parental Rating",
    "Runtime",
    "Rating",
    "Language",
    "Genres",
    "Directors",
    "Actors",
    "Description",
    "URL",
]

filepath: str = "/home/main/PythonProjects/MovieRecommender/data/MetaDataCSV/"
