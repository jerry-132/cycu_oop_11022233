import geopandas as gpd
import matplotlib.pyplot as plt

def plot_bus_stops(geojson_file):
    """
    Plot a map of bus stops (without displaying stop names).
    
    :param geojson_file: Path to the GeoJSON file
    """
    # Read the GeoJSON file
    gdf = gpd.read_file(geojson_file)

    # Check if the data was loaded correctly
    if gdf.empty:
        print("Unable to read the GeoJSON file or the file is empty.")
        return

    # Plot the map
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='blue', markersize=10, alpha=0.7, label='Bus Stops')

    # Set map title and legend
    ax.set_title("Bus Stops Map", fontsize=16)
    ax.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    # Show the map
    plt.show()

# Main program
if __name__ == "__main__":
    geojson_file = "bus_stop2.geojson"  # Ensure the file path is correct
    plot_bus_stops(geojson_file)