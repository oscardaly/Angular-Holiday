from flask import Blueprint, jsonify, make_response, request
from setup_mongodb import config, helpers

cities_blueprint = Blueprint('cities', __name__)
BASE_URL = "/api/v1.0/cities"


@cities_blueprint.route(BASE_URL+ "/get-countries", methods=["GET"])
def get_all_countries():
    data_to_return = config.cities.distinct('country')
    return make_response(jsonify( data_to_return ), 200)

@cities_blueprint.route(BASE_URL, methods=["GET"])
def get_cities_by_country():
    country = None

    if request.args.get('country'):
        country = request.args.get('country')
    
    if country is not None:
        try:
            data_to_return = []
            cities = config.cities.find({'country' : country}, {"city_ascii" : 1, "_id" : 0})
            
            for city in cities:
                data_to_return.append(city['city_ascii'])

            return make_response(jsonify( data_to_return ), 200)

        except:
            return make_response(jsonify({ "error" : "Cities not found" }), 404)

    else:
        return make_response(jsonify({ "error" : "Missing form data" }), 404)


@cities_blueprint.route(BASE_URL + "/<string:cityName>", methods=["GET"])
def get_city_by_name(cityName):
    try:
        city = config.cities.find_one({'city_ascii' : cityName})
        city = helpers.parse_city(city)
        
        if city is not None:
            return make_response(jsonify(city), 200)

        else:
            return make_response(jsonify({ "error" : "City not found" }), 404) 
    
    except:
        return make_response(jsonify({ "error" : "Error when processing request" }), 500)