import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

def coordinates_in_city(lat,lon,city="Marseille"):
	# Les coordonnées sont en (lat,lon) mais les limites trouvées sont en (lon,lat)
	point = Point(lon,lat)
	with open('Tool/limit_marseille.json') as json_file:
		data = json.load(json_file)
		city_limits = list(filter(lambda feature: feature['properties']['nom'] == city, data['features']))
	data_polygons = city_limits[0]["geometry"]['coordinates']
	polygons = []
	for data_polygon in data_polygons:
		polygon = Polygon(data_polygon[0])
		polygons.append(polygon)
	multipolygon = MultiPolygon(polygons)
	return multipolygon.contains(point)