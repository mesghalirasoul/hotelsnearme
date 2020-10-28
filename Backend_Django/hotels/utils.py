
import requests
import os
import json

# class HereApiService:
#     def __init__(self, latitude, longitude, locationname):
#         self.latitude = latitude
#         self.longitude = longitude
#         self.locationname = locationname

def HereApiService(Locationtype, Lat, Long):

    APIKEY = os.environ.get("APIKEY", "localhost")
    url = f'https://places.ls.hereapi.com/places/v1/autosuggest?at={Lat},{Long}&q={Locationtype}&apiKey={APIKEY}'

    response=requests.get(url)
    data = json.loads(response.text)

    data = json.loads(response.text)   

    result = []

    for place in data["results"]:
        if not "position" in place or not "id" in place:
            continue
        else:
            response = {}
            response["title"] = place["title"]
            response["latitude"] = place["position"][0] if 'position' in place else 0
            response["longitude"] = place["position"][1] if 'position' in place else 0
            response["property_id"] = place["id"]
            response["distance"] = place["distance"]
            result.append(response)

    return result
    