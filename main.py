import folium
import csv

def plot_map(coords, popup_data):
    m = folium.Map(location=coords[0], zoom_start=3)
    for (lat, lon), popup_text in zip(coords, popup_data):
        folium.Marker([lat, lon], popup=popup_text).add_to(m)
    folium.PolyLine(coords, color="blue", weight=2.5, opacity=1).add_to(m)
    return m

trainNumber = input('Enter train number: ')
coords = []
popup_data = []

with open(f'{trainNumber}.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            lat = float(row[5])
            lon = float(row[6])
            coords.append([lat, lon])
            popup_data.append(row[7])
        except (ValueError, IndexError):
            print(f"Skipping invalid row: {row}")

map_obj = plot_map(coords, popup_data)
map_obj.save("map.html")