import pandas as pd
from geopy.distance import distance
from geopy.geocoders import Nominatim

# Global cache for geocoding results
geocode_cache = {}

def has_walmart(city_name, threshold=10):
    """
    Determine whether a given city has a Walmart within the specified distance (default 10 miles).

    This function geocodes the city to obtain its coordinates, then reads the Walmart store locations
    CSV, calculates the distance to each store, and returns "Yes" if any store is within the threshold,
    otherwise returns "No".

    Args:
        city_name (str): Name of the city.
        threshold (float, optional): Distance threshold in miles. Defaults to 10.

    Returns:
        str: "Yes" if a Walmart is within the threshold; otherwise, "No".
    """
    # Check cache first
    if city_name in geocode_cache:
        location = geocode_cache[city_name]
    else:
        geolocator = Nominatim(user_agent="demographic_app")
        try:
            location = geolocator.geocode(city_name + ", USA", timeout=10)
        except Exception as e:
            print(f"Geocoding error for {city_name}: {e}")
            return "No"
        if location is None:
            print(f"Could not geocode {city_name}")
            return "No"
        geocode_cache[city_name] = location

    city_coords = (location.latitude, location.longitude)
    
    try:
        # Update this path to point to your CSV file location.
        df = pd.read_csv("/Users/neikkasmith/Demographic/walmart_locations.csv")
    except Exception as e:
        print("Error reading Walmart locations CSV:", e)
        return "No"
    
    # Check that the required columns exist
    expected_columns = ["latitude", "longitude"]
    for col in expected_columns:
        if col not in df.columns:
            print(f"Expected column '{col}' not found in CSV. Found columns: {df.columns.tolist()}")
            return "No"
    
    # Calculate distances from the city to each Walmart store
    df["Distance"] = df.apply(
        lambda row: distance(city_coords, (row["latitude"], row["longitude"])).miles,
        axis=1
    )
    
    if (df["Distance"] <= threshold).any():
        return "Yes"
    else:
        return "No"