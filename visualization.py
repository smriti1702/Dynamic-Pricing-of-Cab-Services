import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Merged Dataset
file_path = r"C:\Users\Smriti Singh\OneDrive\Desktop\Program\ML_Project\merged_dataset.csv"
df = pd.read_csv(file_path)

# Convert timestamps to datetime
df['time_stamp_x'] = pd.to_datetime(df['time_stamp_x'], errors='coerce')

# 1. PRICE DISTRIBUTION
plt.figure(figsize=(8, 5))
plt.hist(df["price"], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Distribution of Ride Prices")
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 2. PRICE VS. WEATHER CONDITIONS (Using Rain Instead)
plt.figure(figsize=(8, 5))

# Define rain categories: No Rain (0) vs. Rain (>0)
df["rain_category"] = df["rain"].apply(lambda x: "No Rain" if x == 0 else "Rain")

# Boxplot
unique_conditions = df["rain_category"].unique()
x_positions = np.arange(len(unique_conditions))
boxplot_data = [df[df["rain_category"] == condition]["price"].dropna() for condition in unique_conditions]

plt.boxplot(boxplot_data, labels=unique_conditions, patch_artist=True)
plt.title("Impact of Rain on Ride Prices")
plt.xlabel("Rain Category")
plt.ylabel("Price ($)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 3. PEAK HOURS ANALYSIS
df["hour"] = df["time_stamp_x"].dt.hour
average_price_per_hour = df.groupby("hour")["price"].mean()

plt.figure(figsize=(8, 5))
plt.plot(average_price_per_hour.index, average_price_per_hour.values, marker="o", linestyle="-", color='red')
plt.title("Average Price at Different Hours of the Day")
plt.xlabel("Hour of the Day")
plt.ylabel("Average Price ($)")
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# 4. DEMAND PATTERN BY DAY OF WEEK
df["day_of_week"] = df["time_stamp_x"].dt.day_name()
average_price_per_day = df.groupby("day_of_week")["price"].mean()
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

plt.figure(figsize=(8, 5))
plt.bar(days_order, [average_price_per_day.get(day, 0) for day in days_order], color="purple", alpha=0.7)
plt.title("Ride Prices Across Days of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Average Price ($)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 5. PRICE VARIATION ACROSS LOCATIONS
unique_destinations = df["destination"].unique()
x_positions = np.arange(len(unique_destinations))
boxplot_data = [df[df["destination"] == dest]["price"].dropna() for dest in unique_destinations]

plt.figure(figsize=(10, 5))
plt.boxplot(boxplot_data, labels=unique_destinations, patch_artist=True)
plt.title("Price Variations Across Destinations")
plt.xlabel("Destination")
plt.ylabel("Price ($)")
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 6. CORRELATION HEATMAP (Without Seaborn)
correlation_matrix = df.corr()

fig, ax = plt.subplots(figsize=(8, 5))
cax = ax.matshow(correlation_matrix, cmap="coolwarm")
plt.colorbar(cax)

ax.set_xticks(np.arange(len(correlation_matrix.columns)))
ax.set_yticks(np.arange(len(correlation_matrix.columns)))
ax.set_xticklabels(correlation_matrix.columns, rotation=90)
ax.set_yticklabels(correlation_matrix.columns)

plt.title("Correlation Heatmap of Dataset", pad=20)
plt.show()
