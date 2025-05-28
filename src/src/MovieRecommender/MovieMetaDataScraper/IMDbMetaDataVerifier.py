import IMDbMetaDataScraper
import pandas as pd
import variables


# Verifies Missing Meta Data
def verify_meta_data(filename) -> None:
    my_csv: pd.DataFrame() = pd.read_csv(filename)

    driver = IMDbMetaDataScraper.start_driver()

    index: int = 0
    meta_datas_adjusted: int = 0

    while index < len(my_csv):
        movie_data: dict = my_csv.iloc[index].to_dict()
        print(movie_data)

        if any(pd.isna(value) for value in movie_data.values()):
            print(f"Adjusting{movie_data.get('Title')}")

            url = movie_data.get("URL")
            driver.get(url)

            movie_data = IMDbMetaDataScraper.grab_meta_data(driver, url)

            meta_datas_adjusted += 1

        my_csv.isetitem(index, movie_data)

        index += 1

    driver.quit()

    print(f"Adjusted {meta_datas_adjusted} movie's metadata information")

    IMDbMetaDataScraper.create_csv()
    IMDbMetaDataScraper.write_to_csv(my_csv)

    return None


def main() -> None:
    filename: str = variables.filename

    verify_meta_data(filename)

    return None


if __name__ == "__main__":
    main()
