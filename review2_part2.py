import os
import sys
import pandas as pd

# Fix encoding issue on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Set working directory
os.chdir(r"C:\Users\Smriti Singh\OneDrive\Desktop\Program\ML_Project")

# Load datasets
cab_rides = pd.read_csv("cab_rides.csv")
dynamic_pricing = pd.read_csv("dynamic_pricing.csv")
weather_data = pd.read_csv("weather_data.csv")

# Fix timestamps if needed
def fix_timestamps(df, column):
    if df[column].max() > 1e10:
        print(f"Converting {column} from milliseconds to seconds...")
        df[column] = df[column] // 1000  
    df[column] = pd.to_datetime(df[column], unit='s', errors='coerce')  
    return df

cab_rides = fix_timestamps(cab_rides, "time_stamp")
weather_data = fix_timestamps(weather_data, "time_stamp")

# Drop invalid timestamps
cab_rides.dropna(subset=["time_stamp"], inplace=True)
weather_data.dropna(subset=["time_stamp"], inplace=True)

# Merge
cab_rides["merge_id"] = cab_rides["destination"].str.strip() + "_" + cab_rides["time_stamp"].dt.strftime("%Y-%m-%d %H")
weather_data["merge_id"] = weather_data["location"].str.strip() + "_" + weather_data["time_stamp"].dt.strftime("%Y-%m-%d %H")
dynamic_pricing["merge_id"] = dynamic_pricing["Location_Category"].str.strip() + "_" + dynamic_pricing["Time_of_Booking"].astype(str)

merged_df = cab_rides.merge(weather_data, on="merge_id", how="left").merge(dynamic_pricing, on="merge_id", how="left")

# Save dataset
merged_df.to_csv("merged_dataset.csv", index=False)
print("\n✅ Merged dataset saved as merged_dataset.csv")


# Load dataset (replace 'merged_dataset.csv' with your actual file path)
df = pd.read_csv("merged_dataset.csv")

# Fix column names by stripping spaces and handling missing headers
df.columns = df.columns.str.strip()

# Convert 'time_stamp' to datetime if applicable
if 'time_stamp' in df.columns:
    df['time_stamp'] = pd.to_datetime(df['time_stamp'], errors='coerce', unit='s')

# Handle missing values
for col in df.columns:
    if df[col].dtype == 'object':  # For categorical columns
        df[col].fillna("Unknown", inplace=True)
    else:  # For numerical columns
        df[col].fillna(df[col].median(), inplace=True)

# Ensure numerical columns are correctly typed
for col in df.select_dtypes(include=['object']).columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except ValueError:
        pass  # Ignore non-numeric columns

# Save cleaned dataset
df.to_csv("cleaned_merged_dataset.csv", index=False)
print("✅ Cleaned dataset saved as 'cleaned_merged_dataset.csv'")
