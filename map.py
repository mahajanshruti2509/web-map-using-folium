import folium
import pandas
import shutil

map = folium.Map(location = [38.58, -99.09], zoom_start = 6)
data = pandas.read_csv("Volcanoes.txt")
latitude = list(data["LAT"])
longitude = list(data["LON"])
elevation = list(data["ELEV"])
name = list(data["NAME"])
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

fgv =  folium.FeatureGroup(name = "Volcanoes")
for lat, lon, elev, name in zip(latitude, longitude, elevation, name):
    iframe = folium.IFrame(html= html % (name, name, elev), width= 200, height= 100)
    fgv.add_child(folium.CircleMarker(location = [lat, lon], radius= 10, popup= folium.Popup(iframe), fill_color= color_producer(elev), color='grey',
    fill_opacity= 0.7))

fgp =  folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding= 'utf-8-sig').read(),
style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000
else 'orange' if 1000000<= x['properties']['POP2005'] < 2000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map.html")
shutil.copy('Map.html', 'templates/Map.html')
