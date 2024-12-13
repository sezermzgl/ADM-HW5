import folium
from tqdm import tqdm


def create_interactive_map(data, passenger_flow):
    """
    Create an interactive map showing the geographic spread of the flight network.

    Args:
        data (pd.DataFrame): Dataset containing latitude/longitude for origin/destination airports.
        passenger_flow (pd.Series): Total passenger flow for each route.

    Outputs:
        Saves an interactive map as an HTML file.
    """
    # Drop rows with missing coordinates
    data = data.dropna(
        subset=[
            "Org_airport_lat",
            "Org_airport_long",
            "Dest_airport_lat",
            "Dest_airport_long",
        ]
    )

    # Drop duplicate routes, aggregate passenger flow, and filter out zero-passenger routes
    data = (
        data.groupby(
            [
                "Origin_airport",
                "Destination_airport",
                "Org_airport_lat",
                "Org_airport_long",
                "Dest_airport_lat",
                "Dest_airport_long",
            ]
        )["Passengers"]
        .sum()
        .reset_index()
    )

    # Filter out routes with total passengers = 0
    data = data[data["Passengers"] > 0]

    # Initialize a larger folium map
    m = folium.Map(
        location=[37.7749, -122.4194],  # Centered around the US
        zoom_start=5,
        width="100%",  # Set to 100% of the window width
        height="100%",  # Set to 100% of the window height
    )

    # Add a progress bar for route processing
    print("Processing routes for map...")
    for _, row in tqdm(data.iterrows(), total=len(data)):
        # Extract coordinates and passenger data
        org_lat = row["Org_airport_lat"]
        org_long = row["Org_airport_long"]
        dest_lat = row["Dest_airport_lat"]
        dest_long = row["Dest_airport_long"]
        passengers = row["Passengers"]

        # Add the route to the map
        folium.PolyLine(
            locations=[[org_lat, org_long], [dest_lat, dest_long]],
            color="blue",
            weight=2,
            tooltip=f"{row['Origin_airport']} -> {row['Destination_airport']}: {passengers} passengers",
        ).add_to(m)

    # Save the map as an HTML file
    map_filename = "flight_network_map.html"
    m.save(map_filename)
    print(f"Interactive map saved as '{map_filename}'")
