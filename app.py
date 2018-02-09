#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

## Hatem dealing with google places api ########################
from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyADsZZiGIWF2laJkl5qNE5EUkSXkye4HG4'
robot_photo_url = "https://cdn.pixabay.com/photo/2014/04/03/11/55/robot-312566_960_720.png"

google_places = GooglePlaces(YOUR_API_KEY)

################################################################

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("city")

    resolvedQuery = parameters.get("resolvedQuery")
    attraction = parameters.get("attraction")    

   ##############################Hatem
   # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
        location=city, keyword=attraction,
        radius=20000) #, types=[types.TYPE_FOOD])
    
    #xplace = query_result.html_attributions
    for place in query_result.places:
        #Returned places from a query are place summaries.
        place_name = place.name
        place_geo_loc = place.geo_location
        place_id = place.place_id
        place.get_details()
        place_url=place.url
        
        place_photos=place.photos
        #place_photos_ref=place_photos[0].photo_reference
        print(place_photos)
        
        #p1=place_photos.get
        p2=place_photos.getUrl()
        #p3=p1.url
        print(p2)
        #print(p3)
     
        
        
        #wasfy test
        #photo_url=place.photos[0].url
        #place_phoo=place.photos
        
        #place_photo=place_phoo[0]
        
        #place_photo_url=place_photo.url
        
        
        #Getting place photos

        ###for photo in place.photos:
            # 'maxheight' or 'maxwidth' is required
            ###place_photo = 
            ###photo.get(maxheight=500, maxwidth=500)
            # MIME-type, e.g. 'image/jpeg'
            #place_mime = 
            ###photo.mimetype
            # Image URL
            ###
            ###place_photo_url=photo.url
            # Original filename (optional)
            ###place_photo_name = photo.filename
            # Raw image data
            ###place_photo_data = photo.data
            
            
                
        
    
   ##############################Hatem

    ###speech = "There are nice" + attraction #+ "places in " + city + "to have" + resolvedQuery + " and I will tell you about them. " #+ str(cost[zone])
    ##working### speech = "There are nice places in " + city + " and I will tell you about them. "
    #speech = "There are nice " + attraction + " to have " + resolvedQuery + "places in " + city + " and I will tell you about them. "
    #speech = "There are nice places in " + city + attraction + resolvedQuery + " and I will tell you about them. "
    
    ###working###
    #speech = "Hmm, I'll tell you about the best places in " + city + " to have " + attraction
    #############
    
    #hatem
    #speech = "Hmm, I'll tell you about the best places in " + city + " to have " + attraction + ", how about: " + place_name + " and its address is: " place_geo_loc
    speech = "Hmm, I'll tell you about the best places in " + city + " to have " + attraction + ".\nHow about: " + place_name + "? \nCheck its info here: \n" + place_url
## + " and its address is: " place_geo_loc

    ####
    
    
    print("Response:")
    print(speech)
    ###return {
        ###"speech": speech,
        ###"displayText": speech,
        #"data": {},
        #"contextOut": [],
        ##"source": "travelsourse"
    ###}

#########

##--> RETURN
    return {
        "speech": speech,
        "displayText": speech,
        "messages":[
        {
            "type": 3,
            "imageUrl":robot_photo_url
        },
            {
                "type": 0,
                "speech": speech
            },
            {
                "type": 2,
                "title": "Is it useful to you?",
                "replies": [
                    "Yes",
                    "No",
                    "I don't know"
                ]
            }
        ]
        #"data": {},
        #"contextOut": [],
        ##"source": "travelsourse"
    }


###########################################
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
