import pandas as pd
import variables


# Splits the CSV file into separate CSV files by column
def split_csv_by_column(filename) -> None:
    # Read the CSV file
    my_csv = pd.read_csv(filename)

    # Grabs Title Column to have a label for each metadata entry
    title_column: pd.DataFrame = pd.DataFrame(my_csv[["Title"]])

    # Iterates through each column,
    # then appends the title column and metadata column to new CSV
    for column in my_csv.columns[1:]:
        column_data: pd.DataFrame = pd.DataFrame(my_csv[column])
        output_data: pd.DataFrame = pd.DataFrame()

        output_data = pd.concat([title_column, column_data], axis=1)

        output_data.to_csv(
            f"/home/main/PythonProjects/MovieRecommender/data/MetaDataCSV/{column}.csv",
            index=False,
            encoding="utf-8",
        )

        print(f"Saved {column}.csv")
        print(output_data)

    print(f"Split {filename} into separate CSV files by column.")

    return None


def expand_data(filename) -> None:
    data: pd.DataFrame = pd.read_csv(filename)
    data_expanded: pd.DataFrame = pd.DataFrame()

    index: int = 0
    data_type: str = filename.split("/")[-1].split(".")[0]

    while index < len(data):
        movie_info: dict = data.iloc[index].to_dict()
        print(movie_info)
        data_str: str = movie_info.get(data_type)
        data_list: list = []

        if pd.isna(data_str):
            print(
                f"Skipping row {index}: Missing or invalid data in column '{data_type}'"
            )
            index += 1
            continue

        if data_type == "Genres" or data_type == "Language":
            data_list = data_str.split(", ")

        elif data_type == "Actors" or data_type == "Directors":
            last_break: int = 0

            for i in range(len(data_str) - 1):
                if data_str[i].islower() and data_str[i + 1].isupper():
                    temp_str: str = data_str[last_break:i]
                    data_list.append(temp_str)
                    last_break = i

            if not data_list:
                data_list.append(data_str)

        else:
            print("Not an acceptable file.")
            break

        new_movie_info_dict: dict = {}
        new_movie_info_dict["Title"] = movie_info.get("Title")

        new_movie_info_dict[data_type] = data_list

        new_movie_info_dataframe: pd.DataFrame = pd.DataFrame([new_movie_info_dict])
        # print(new_movie_info_dataframe)

        data_expanded: pd.DataFrame = pd.concat(
            [data_expanded, new_movie_info_dataframe], ignore_index=True
        )
        index += 1

    data_expanded.to_csv(
        f"/home/main/PythonProjects/MovieRecommender/data/MetaDataCSV/{data_type}_Expanded.csv",
        index=False,
        encoding="utf-8",
    )

    return None


def main() -> None:
    filename = variables.filepath + "imdbData.csv"
    genres_file = variables.filepath + "Genres.csv"
    actors_file = variables.filepath + "Actors.csv"
    directors_file = variables.filepath + "Directors.csv"
    languages_file = variables.filepath + "Language.csv"

    split_csv_by_column(filename)

    print(genres_file)
    expand_data(genres_file)
    expand_data(actors_file)
    expand_data(directors_file)
    expand_data(languages_file)

    return None


if __name__ == "__main__":
    main()
