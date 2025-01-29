import googlemaps


GMAPS_API_KEY = "AIzaSyCK_dd-qY0FadiLl7idwLnxA3M9A7tgyRs"
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

def get_coordinates(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        location = geocode_result[0]["geometry"]["location"]
        place = f"{location['lat']},{location['lng']}"

        return f"https://www.google.com/maps/embed/v1/place?key={GMAPS_API_KEY}&q={place}"
    return None
