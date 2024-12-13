import numpy as np


def analyze_graph_features(flight_network, data):
    """
    Analyze the flight network graph based on the requirements.

    Args:
        flight_network (nx.DiGraph): Directed graph representing the flight network.
        data (pd.DataFrame): Dataset containing flight details (e.g., passengers, flights).

    Returns:
        dict: Dictionary containing analysis results:
            - num_nodes: Number of nodes
            - num_edges: Number of edges
            - density: Graph density
            - in_degrees: Dictionary of in-degrees for each node
            - out_degrees: Dictionary of out-degrees for each node
            - hubs: List of hub nodes (90th percentile of degree)
            - passenger_flow: Total passenger flow for each route
            - avg_passengers_per_flight: Average passengers per flight for each route
    """
    # 1. Graph properties
    num_nodes = len(flight_network.nodes)
    num_edges = len(flight_network.edges)

    if num_nodes > 1:
        density = (2 * num_edges) / (num_nodes * (num_nodes - 1))
    else:
        density = 0

    # 2. In-degree and out-degree
    in_degrees = {node: 0 for node in flight_network.nodes}
    out_degrees = {node: 0 for node in flight_network.nodes}
    for edge in flight_network.edges:
        out_degrees[edge[0]] += 1
        in_degrees[edge[1]] += 1

    # 3. Hubs (90th percentile)
    all_degrees = {
        node: in_degrees[node] + out_degrees[node] for node in flight_network.nodes
    }
    degree_threshold = np.percentile(list(all_degrees.values()), 90)
    hubs = [node for node, degree in all_degrees.items() if degree > degree_threshold]

    # 4. Total passenger flow and average passengers per flight
    passenger_flow = data.groupby(["Origin_airport", "Destination_airport"])[
        "Passengers"
    ].sum()
    avg_passengers_per_flight = (
        data.groupby(["Origin_airport", "Destination_airport"])[
            ["Passengers", "Flights"]
        ]
        .sum()
        .eval("Passengers / Flights")
    )

    # Results
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "in_degrees": in_degrees,
        "out_degrees": out_degrees,
        "hubs": hubs,
        "passenger_flow": passenger_flow,
        "avg_passengers_per_flight": avg_passengers_per_flight,
    }
