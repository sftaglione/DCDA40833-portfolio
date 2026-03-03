import pandas as pd
import requests
import folium

# 🔑 YOUR MAPBOX TOKEN
access_token = ""

# 📍 Load your CSV
df = pd.read_csv("hometown_locations.csv")

# 🌍 Function to get lat/lon from address
def geocode(address):
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={address}&access_token={access_token}"
    response = requests.get(url)
    data = response.json()

    if "features" in data and len(data["features"]) > 0:
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords[1], coords[0]
    else:
        print(f"Geocode failed for: {address}")
        return None, None

# ➕ Add lat/lon to dataframe
df["Latitude"], df["Longitude"] = zip(*df["Address"].apply(geocode))

# 🗺️ Create map (centered on Dana Point)
m = folium.Map(location=[33.466, -117.698], zoom_start=13)

# 🎨 Color by type
def get_color(type):
    if type == "Restaurant":
        return "red"
    elif type == "Cafe":
        return "blue"
    elif type == "Beach":
        return "green"
    else:
        return "purple"

# 📍 Add markers
for i, row in df.iterrows():
    if pd.notnull(row["Latitude"]):
        popup_html = f"""
        <h4>{row['Name']}</h4>
        <p>{row['Description']}</p>
        <img src="{row['Image_URL']}" width="200">
        """
        
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=get_color(row["Type"]))
        ).add_to(m)

# 💾 Save map
m.save("hometown_map.html")

print("Map created!")