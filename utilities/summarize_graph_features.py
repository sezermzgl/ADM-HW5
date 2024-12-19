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
        - Busiest routes table and bar chart
        - Over/under-utilized routes table and bar chart
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
    print("\nHubs (airports above the 90th percentile):")
    hubs_df = pd.DataFrame(analysis_results["hubs"], columns=["Hub Airports"])
    # print(
    #     hubs_df.to_string(index=False)
    # )  # Display the DataFrame in a clear table format

    # 4. Top routes by passenger flow
    passenger_flow = analysis_results["passenger_flow"].nlargest(10)
    passenger_flow_df = passenger_flow.reset_index()
    passenger_flow_df.columns = ["Origin", "Destination", "Total Passengers"]
    passenger_flow_df["Route"] = (
        passenger_flow_df["Origin"] + " -> " + passenger_flow_df["Destination"]
    )
    passenger_flow_df = passenger_flow_df[
        ["Route", "Total Passengers"]
    ]  # Keep only relevant columns
    print("\nTop 10 busiest routes by passenger flow:")
    # print(passenger_flow_df.to_string(index=False))  # Display as a clean table
    passenger_flow_df.plot(
        kind="bar",
        x="Route",
        y="Total Passengers",
        figsize=(10, 6),
        title="Top 10 Busiest Routes",
    )
    plt.ylabel("Total Passengers")
    plt.show()

    # 5. Top routes by passenger efficiency
    avg_passengers_per_flight = analysis_results["avg_passengers_per_flight"].nlargest(
        10
    )
    avg_efficiency_df = avg_passengers_per_flight.reset_index()
    avg_efficiency_df.columns = [
        "Origin",
        "Destination",
        "Average Passengers per Flight",
    ]
    avg_efficiency_df["Route"] = (
        avg_efficiency_df["Origin"] + " -> " + avg_efficiency_df["Destination"]
    )
    avg_efficiency_df = avg_efficiency_df[
        ["Route", "Average Passengers per Flight"]
    ]  # Keep only relevant columns
    print("\nTop 10 routes by passenger efficiency:")
    # print(avg_efficiency_df.to_string(index=False))  # Display as a clean table
    avg_efficiency_df.plot(
        kind="bar",
        x="Route",
        y="Average Passengers per Flight",
        figsize=(10, 6),
        title="Top 10 Efficient Routes",
    )
    plt.ylabel("Average Passengers per Flight")
    plt.show()

    return hubs_df, passenger_flow_df, avg_efficiency_df
