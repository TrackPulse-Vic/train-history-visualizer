import folium
import csv
import os
from dotenv import load_dotenv

# Ensure thunderforest api key is set
load_dotenv()
if not os.getenv('THUNDERFOREST_KEY'):
    raise ValueError("Thunderforest API key is not set in the environment. Please set it in the .env file.")    

def plot_map(coords, popup_data, line_names, color_map):
    m = folium.Map(location=coords[0], zoom_start=10, 
                  tiles='https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey='+ os.getenv('THUNDERFOREST_KEY'), 
                  attr='Maps © Thunderforest, Data © OpenStreetMap contributors')
    
    for (lat, lon), popup_text in zip(coords, popup_data):
        folium.Marker([lat, lon], popup=popup_text).add_to(m)
    
    current_line = line_names[0]
    segment_coords = [coords[0]]
    
    for i in range(1, len(coords)):
        if line_names[i] != current_line:
            segment_coords.append(coords[i-1])
            line_color = color_map.get(current_line, '#FFFF00')  # Default to yellow if not found
            folium.PolyLine(segment_coords, color=line_color, weight=2.5, opacity=1).add_to(m)
            
            segment_coords = [coords[i-1]]
            current_line = line_names[i]
        segment_coords.append(coords[i])
    
    line_color = color_map.get(current_line, '#FFFF00')
    folium.PolyLine(segment_coords, color=line_color, weight=2.5, opacity=1).add_to(m)
    
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
line_names = []

with open(f'{trainNumber}.csv', 'r') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        try:
            lat = float(row[5])
            lon = float(row[6])
            coords.append([lat, lon])
            popup_data.append(f'{row[0]} line to {row[4]} | {row[7]}' if len(row) > 7 else f'{row[0]} to {row[4]}')
            line_names.append(row[0])
        except (ValueError, IndexError):
            print(f"Skipping invalid row {i+1}.")

map_obj = plot_map(coords, popup_data, line_names, color_map)
map_obj.save("map.html")