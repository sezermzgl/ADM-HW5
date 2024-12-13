import pandas as pd
import matplotlib.pyplot as plt


def summarize_graph_features(flight_network, analysis_results):
    """
    Generate a detailed report of the graph's features.

    Args:
        flight_network (nx.DiGraph): Directed graph representing the flight network.
        analysis_results (dict): Results from the analyze_graph_features function.

    Outputs:
        - Text summaries
        - Degree distribution histograms
        - Busiest routes bar chart
        - Over/under-utilized routes bar chart
    """
    # 1. Graph properties
    print(f"Number of airports (nodes): {analysis_results['num_nodes']}")
    print(f"Number of flights (edges): {analysis_results['num_edges']}")
    print(f"Graph density: {analysis_results['density']:.4f}")

    # 2. Degree distributions
    in_degrees = analysis_results["in_degrees"]
    out_degrees = analysis_results["out_degrees"]
    plt.hist(list(in_degrees.values()), bins=20, alpha=0.5, label="In-degree")
    plt.hist(list(out_degrees.values()), bins=20, alpha=0.5, label="Out-degree")
    plt.legend(loc="upper right")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree Distribution")
    plt.show()

    # 3. Hubs
    hubs_df = pd.DataFrame(analysis_results["hubs"], columns=["Hub Airports"])
    #print(hubs_df.to_string(index=False))  # Display the DataFrame in a clear table format

    # 4. Busiest routes
    passenger_flow = analysis_results["passenger_flow"].nlargest(10)
    print("\nTop 10 busiest routes by passenger flow:")
    #print(passenger_flow)
    passenger_flow.plot(kind="bar", figsize=(10, 6), title="Top 10 Busiest Routes")
    plt.ylabel("Total Passengers")
    plt.show()

    # 5. Average passengers per flight
    avg_passengers_per_flight = analysis_results["avg_passengers_per_flight"].nlargest(
        10
    )
    print("\nTop 10 routes by passenger efficiency:")
    #print(avg_passengers_per_flight)
    avg_passengers_per_flight.plot(
        kind="bar", figsize=(10, 6), title="Top 10 Efficient Routes"
    )
    plt.ylabel("Average Passengers per Flight")
    plt.show()

    print("\nHubs (airports above the 90th percentile):")
    return hubs_df
