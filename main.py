import folium
import csv
import os
from dotenv import load_dotenv

# Ensure thunderforest api key is set
load_dotenv()
if not os.getenv('THUNDERFOREST_KEY'):
    raise ValueError("Thunderforest API key is not set in the environment. Please set it in the .env file.")    


def plot_map(coords, popup_data, line_color):
    m = folium.Map(location=coords[0], zoom_start=10, tiles='https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey='+ os.getenv('THUNDERFOREST_KEY'), attr='Maps © Thunderforest, Data © OpenStreetMap contributors')
    for (lat, lon), popup_text in zip(coords, popup_data):
        folium.Marker([lat, lon], popup=popup_text).add_to(m)
    folium.PolyLine(coords, color=line_color, weight=2.5, opacity=1).add_to(m)
    return m

color_map = {
    'Lilydale': '#01518a',
    'Belgrave': '#01518a',
    'Glen Waverley': '#01518a',
    'Alamein': '#01518a',
    'Pakenham': '#00a8e4',
    'Cranbourne': '#00a8e4',
    'Frankston': '#009645',
    'Sandringham': '#f4a1c5',
    'Williamstown': '#009645',
    'Werribee': '#009645',
    'Sunbury': '#fcb818',
    'Craigieburn': '#fcb818',
    'Upfield': '#fcb818',
    'Mernda': '#d0202e',
    'Hurstbridge': '#d0202e',
}

trainNumber = input('Enter train number: ')
coords = []
popup_data = []
first_column_value = None

with open(f'{trainNumber}.csv', 'r') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        try:
            if i == 0:
                first_column_value = row[0]
            lat = float(row[5])
            lon = float(row[6])
            coords.append([lat, lon])
            popup_data.append(f'{row[0]} line to {row[4]} | {row[7]}' if len(row) > 7 else f'{row[0]} to {row[4]}')
        except (ValueError, IndexError):
            print(f"Skipping icon on invalid row.")

# Default to blue
line_color = color_map.get(first_column_value, 'YELLOW')
map_obj = plot_map(coords, popup_data, line_color)
map_obj.save("map.html")