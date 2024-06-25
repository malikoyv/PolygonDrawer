import numpy as np

# Google Maps API Key (replace with your own)
API_KEY = 'AIzaSyDHNBJFmuHpGmhaTC5Deo_LBYsjBD1hdEk'

# Coordinates for Gdańsk, Poland
gdansk_coordinates = [
    (54.380125, 18.587927),
    (54.373425, 18.604137),
    (54.375684, 18.629654),
    (54.387119, 18.629246),
    (54.387630, 18.610150)
]


# Function to create a Google Maps Polygon object
def create_polygon(coordinates):
    polygon = {
        "paths": [coordinates],
        "strokeColor": "#FF0000",
        "strokeOpacity": 0.8,
        "strokeWeight": 2,
        "fillColor": "#FF0000",
        "fillOpacity": 0.35,
    }
    return polygon


# Function to calculate area of polygon using geodesic distances
def calculate_polygon_area(coordinates):
    def geodesic_area(lats, lons):
        # Convert latitude and longitude to radians
        lats = np.radians(lats)
        lons = np.radians(lons)

        # Earth radius in kilometers
        R = 6371.0

        # Initialize area
        area = 0.0

        for i in range(len(lats)):
            lat1, lon1 = lats[i], lons[i]
            lat2, lon2 = lats[(i + 1) % len(lats)], lons[(i + 1) % len(lats)]
            # Shoelace formula on a sphere
            area += (lon2 - lon1) * (2 + np.sin(lat1) + np.sin(lat2))

        # Final area in square kilometers
        area = area * (R**2) / 2.0
        return round(abs(area), 2)

    lats, lons = zip(*coordinates)
    return geodesic_area(lats, lons)


# Function to generate HTML file with Google Maps visualization
def generate_html(polygons):
    template = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Google Maps Polygons</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={}&libraries=drawing"></script>
        <script>
          function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
              zoom: 12,
              center: {{lat: 54.4009, lng: 18.6446}}
            }});

            {}
          }}
        </script>
      </head>
      <body onload="initMap()">
        <div id="map" style="height: 600px; width: 100%;"></div>
      </body>
    </html>
    """

    polygons_js = []
    for polygon in polygons:
        coordinates_js = ",".join([f"{{lat: {lat}, lng: {lng}}}" for lat, lng in polygon['paths'][0]])
        polygons_js.append(f"""
            var polygon = new google.maps.Polygon({{
              paths: [{coordinates_js}],
              strokeColor: '{polygon['strokeColor']}',
              strokeOpacity: {polygon['strokeOpacity']},
              strokeWeight: {polygon['strokeWeight']},
              fillColor: '{polygon['fillColor']}',
              fillOpacity: {polygon['fillOpacity']}
            }});
            polygon.setMap(map);
        """)

    with open('google_maps_polygons.html', 'w') as f:
        f.write(template.format(API_KEY, "\n".join(polygons_js)))

    print("HTML file generated: google_maps_polygons.html")


# Main function
def main():
    # Create polygon for Gdańsk
    polygon = create_polygon(gdansk_coordinates)
    polygons = [polygon]

    # Calculate area of Gdańsk polygon
    area = calculate_polygon_area(gdansk_coordinates)
    print(f"Area of Gdańsk Polygon: {area} square kilometers")

    # Generate HTML file with Google Maps visualization
    generate_html(polygons)


if __name__ == "__main__":
    main()