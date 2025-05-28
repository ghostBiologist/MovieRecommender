import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import variables_genres as vg
from sklearn.metrics.pairwise import cosine_similarity


# Loads movie title and genres into dataframe
def load_data(filename) -> pd.DataFrame:
    genre_data: pd.DataFrame = pd.read_csv(filename)
    return genre_data


# Defines type of weighted decay applied to the movie genres based on number of genres
def position_weights(
    number_genres: int, decay_type: str, decay_rate: float
) -> np.array:
    positions = np.linspace(0, 1, number_genres)
    weights: np.array = []

    if decay_type == "reciprocal":
        weights = np.array([1 / (i + 1) for i in range(number_genres)])

    elif decay_type == "exponential":
        weights = np.exp(-decay_rate * positions)

    elif decay_type == "linear":
        weights = positions

    return weights


# Transforms genres into weighted matrix from above weights
def pre_process_data(
    genre_data_expanded: pd.DataFrame, decay_type: str, decay_rate: float = 1.0
) -> np.array:
    all_genres: list = sorted(
        {g for genres in genre_data_expanded.get("Genres") for g in genres}
    )

    # print("All Genres:")
    # print(all_genres)

    all_genres_dict: dict = {g: i for i, g in enumerate(all_genres)}

    number_movies: int = len(genre_data_expanded)

    number_genres: int = len(all_genres)

    weighted_matrix: np.array = np.zeros((number_movies, number_genres))

    for row, movie_data in genre_data_expanded.iterrows():
        genres: list = movie_data["Genres"]
        weights: np.array = position_weights(len(genres), decay_type, decay_rate)

        for j, genre in enumerate(genres):
            weighted_matrix[row, all_genres_dict[genre]] = weights[j]

    # print(f"\n\nThis is the weighted matrix for a(n) {decay_rate} decay")
    # print(weighted_matrix)

    return weighted_matrix


# Computes the similarity between different movies based on the genres
def compute_cosine_similarity_matrix(weighted_matrix: np.array) -> cosine_similarity:
    sims: cosine_similarity = cosine_similarity(weighted_matrix)

    # print(sims)

    return sims


# Builds a network for the movies
def build_network_graph(
    sims: cosine_similarity, titles: list, edge_threshold: float
) -> nx.Graph():
    my_network: nx.Graph() = nx.Graph()
    my_network.add_nodes_from(titles)

    number_titles: int = len(titles)
    for i in range(number_titles):
        for j in range(i + 1, number_titles):
            if sims[i, j] > edge_threshold:
                my_network.add_edge(titles[i], titles[j], weight=sims[i, j])

    return my_network


# Detects communities in network based with greedy modularity algorithm
def detect_communities_greedy_modularity(my_network: nx.Graph):
    comms = nx.community.greedy_modularity_communities(my_network)

    return comms


# Detects communities in network based on girvan newman algorithm
def detect_communities_girvan_newman(my_network: nx.Graph):
    comms = nx.community.girvan_newman(my_network)

    return comms


# Plots the network
def plot_graph(my_network: nx.Graph(), comm_det_algo_type: str) -> None:
    if comm_det_algo_type == "greedy":
        comms = detect_communities_greedy_modularity(my_network)
        node_comms = [list(comm) for comm in comms]

    elif comm_det_algo_type == "girvan":
        comms = detect_communities_girvan_newman(my_network)
        node_comms = [list(comm) for comm in next(comms)]

    colors: list = [
        "red",
        "blue",
        "green",
        "yellow",
        "orange",
        "purple",
        "brown",
        "cyan",
        "magenta",
        "pink",
        "gray",
        "olive",
        "teal",
        "navy",
        "maroon",
        "lime",
        "aqua",
        "silver",
        "indigo",
        "violet",
        "coral",
        "gold",
        "plum",
        "chocolate",
    ]
    node_color_mapping: list = []

    # print(node_comms)

    for node in my_network:
        for i, group in enumerate(node_comms):
            if node in group:
                node_color_mapping.append(colors[i])

    pos = nx.spring_layout(my_network, k=0.8)
    plt.figure(figsize=(100, 100))
    nx.draw(
        my_network,
        pos,
        node_color=node_color_mapping,
        with_labels=True,
        font_color="pink",
        node_size=400,
        font_size=25,
        width=0.2,
        edge_cmap=plt.cm.Blues,
    )
    plt.title("Movie-Genre Similarity Graph", fontsize=80)
    plt.show()

    return None


# Easily call the genre visualizer as one command
def genre_visualizer(
    genre_data_expanded: pd.DataFrame,
    edge_threshold: float,
    decay_type: str,
    comm_det_algo_type: str,
    decay_rate: float = 1.0,
) -> None:
    titles: list = genre_data_expanded.get("Title")

    weighted_matrix: np.array = pre_process_data(
        genre_data_expanded, decay_type, decay_rate
    )

    sims: cosine_similarity = compute_cosine_similarity_matrix(weighted_matrix)

    my_network: nx.Graph = build_network_graph(sims, titles, edge_threshold)

    print(
        f"This network has a(n) {decay_type} decay and uses the {comm_det_algo_type} community detection algorithm. \n"
        + f"It has a {decay_type} decay with a decay rate of {decay_rate}. \n"
        + f"The edge threshold is {edge_threshold}: "
    )

    plot_graph(my_network, comm_det_algo_type)

    return None


def main() -> None:
    my_filename: str = vg.filename
    my_decay_type: str = vg.decay_type
    my_comm_det_algo_type: str = vg.comm_det_algo_type
    my_edge_threshold: float = vg.edge_threshold
    my_decay_rate: float = vg.decay_rate

    my_genre_data_expanded: pd.DataFrame = load_data(my_filename)

    genre_visualizer(
        genre_data_expanded=my_genre_data_expanded,
        edge_threshold=my_edge_threshold,
        decay_type=my_decay_type,
        comm_det_algo_type=my_comm_det_algo_type,
        decay_rate=my_decay_rate,
    )

    return None


if __name__ == "__main__":
    main()
