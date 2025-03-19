import googlemaps
from django.conf import settings

# Setting up the Google Maps API key. Get the 
# key from the settings file.
GMAPS_API_KEY = settings.GOOGLE_MAP_KEY

# Initializing the Google Map Client
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Function to get coordinate form an address
def get_coordinates(address):
    
    #Get Coordinates form an address
    geocode_result = gmaps.geocode(address)

    # Extracting the Latitude and Longitude if result is return
    if geocode_result:
        location = geocode_result[0]["geometry"]["location"]
        place = f"{location['lat']},{location['lng']}"

        return f"https://www.google.com/maps/embed/v1/place?key={GMAPS_API_KEY}&q={place}"
    return None # return null if no data is found
