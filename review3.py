import os
import sys
import pandas as pd

# Fix encoding issue on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Set working directory
os.chdir(r"C:\Users\Smriti Singh\OneDrive\Desktop\Program\ML_Project")

# Load datasets
dynamic_pricing = pd.read_csv("dynamic_pricing.csv")
weather_data = pd.read_csv("weather_with_location_type.csv")  # Updated weather file with location_type

# Strip whitespaces and lowercase for consistency
dynamic_pricing['Location_Category'] = dynamic_pricing['Location_Category'].str.strip().str.lower()
weather_data['location_type'] = weather_data['location_type'].str.strip().str.lower()

# Merge on location type (Urban/Suburban/Rural)
merged_df = pd.merge(dynamic_pricing, weather_data, left_on='Location_Category', right_on='location_type', how='left')

# Fill missing values in the 'rain' column with the median
merged_df['rain'] = merged_df['rain'].fillna(merged_df['rain'].median())

# Save the merged dataset
merged_df.to_csv("dynamic_weather_merged.csv", index=False)
print("✅ Merged dataset saved as 'dynamic_weather_merged.csv'")
