import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import variables_genres
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import MultiLabelBinarizer


def load_data(filename: str) -> pd.DataFrame:
    genre_data: pd.DataFrame = pd.read_csv(filename)
    return genre_data


def expand_data(genre_data: pd.DataFrame) -> pd.DataFrame:
    genre_data_expanded: pd.DataFrame = pd.DataFrame()

    index: int = 0

    while index < len(genre_data):
        movie_info: dict = genre_data.iloc[index].to_dict()
        genre_str: str = movie_info.get("Genres")
        genre_list: list = genre_str.split(", ")

        new_movie_info_dict: dict = {}
        new_movie_info_dict["Title"] = movie_info.get("Title")

        new_movie_info_dict["Genres"] = genre_list

        new_movie_info_dataframe: pd.DataFrame = pd.DataFrame([new_movie_info_dict])
        print(new_movie_info_dataframe)

        genre_data_expanded = pd.concat(
            [genre_data_expanded, new_movie_info_dataframe], ignore_index=True
        )
        index += 1

    genre_data_expanded.to_csv("Expanded_Genres.csv", index=False)

    return genre_data_expanded


def multi_lable_binarize_data(genre_data: pd.DataFrame) -> pd.DataFrame:
    mlb: MultiLabelBinarizer = MultiLabelBinarizer()
    pre_processed_genres: pd.DataFrame = mlb.fit_transform(genre_data["Genres"])

    print(pre_processed_genres)

    return pre_processed_genres


def compute_jacard_index(pre_processed_genres: pd.DataFrame) -> pd.DataFrame:
    dists: pd.DataFrame = pairwise_distances(pre_processed_genres, metric="jaccard")
    sims: pd.DataFrame = 1 - dists

    return sims


def build_network_graph(sims: pd.DataFrame, titles: list) -> nx.Graph():
    threshold: float = 0.3

    my_network: nx.Graph() = nx.Graph()
    my_network.add_nodes_from(titles)

    titles_len: int = len(titles)
    for i in range(titles_len):
        for j in range(i + 1, titles_len):
            if sims[i, j] > threshold:
                my_network.add_edge(titles[i], titles[j], weight=sims[i, j])

    return my_network


def plot_graph(my_network: nx.Graph()) -> None:
    pos = nx.spring_layout(my_network)
    plt.figure(figsize=(100, 100))
    nx.draw(
        my_network,
        pos,
        with_labels=True,
        font_color="pink",
        node_size=500,
        font_size=8,
        edge_cmap=plt.cm.Blues,
    )
    plt.title("Movie-Genre Similarity Graph")
    plt.show()

    return None


def main() -> None:
    filename = variables_genres.filename

    genre_data: pd.DataFrame = load_data(filename)

    genre_data_expanded: pd.DataFrame = expand_data(genre_data)

    pre_processed_genres: pd.DataFrame = multi_lable_binarize_data(genre_data_expanded)

    titles: list = genre_data_expanded["Title"].tolist()
    sims: pd.DataFrame = compute_jacard_index(pre_processed_genres)

    my_network: nx.Graph() = build_network_graph(sims, titles)

    plot_graph(my_network)

    return None


if __name__ == "__main__":
    main()
