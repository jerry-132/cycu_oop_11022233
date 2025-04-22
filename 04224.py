import plot_bus_stops
import json

# Main program
if __name__ == "__main__":
    geojson_file = "bus_stop2.geojson"  # Ensure the file path is correct
    plot_bus_stops.plot_bus_stops(geojson_file)