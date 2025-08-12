import pandas as pd

# Load your actual CSV files
weather_df = pd.read_csv("weather_data.csv")

# Convert location to lowercase for consistent mapping
weather_df['location'] = weather_df['location'].str.strip().str.lower()

# Manual mapping of locations to Urban/Suburban/Rural
location_type_map = {
    "back bay": "Urban",
    "beacon hill": "Suburban",
    "boston university": "Suburban",
    "fenway": "Rural",
    "financial district": "Urban",
    "haymarket": "Rural",
    "north end": "Rural",
    "north station": "Rural"
}

# Map to new column
weather_df["location_type"] = weather_df["location"].map(location_type_map).fillna("Unknown")

# Save to CSV
weather_df.to_csv("weather_with_location_type.csv", index=False)
