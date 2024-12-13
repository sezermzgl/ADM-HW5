import pandas as pd
import networkx as nx


def load_flight_network(filepath):
    """
    Load the flight dataset and build a directed graph.
    """
    data = pd.read_csv(filepath)
    flight_network = nx.DiGraph()

    # Add edges and attributes (Passengers, Flights) from the dataset
    for _, row in data.iterrows():
        flight_network.add_edge(
            row["Origin_airport"],
            row["Destination_airport"],
            Passengers=row["Passengers"],
            Flights=row["Flights"],
        )

    return flight_network, data
