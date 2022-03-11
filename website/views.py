from flask import Blueprint, redirect, render_template, jsonify, request
from flask_login import login_required, current_user
from website.mock_requests.mock_responses import get_api_cell_response
from website.models import MoodTypes, ReturnStatus, get_last_user_data, get_location_distances, mood_frequency
from website.GPS_calculations import Haversine

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():  
    return render_template("home.html", user=current_user)

@views.route('/mood_freq/<user>/', methods=['GET'])
@login_required
def get_mood_frequency( user ):
    """Get total captured mood from every mood type and calculate distribution from a given user
    Keyword arguments:
    user -- user name
    """
    distribution = mood_frequency(user)
    if not distribution:
        return jsonify("Distribution not available"), 404 
    return jsonify(distribution), 200 

@views.route('/happy_dist/<user>/', methods=['GET'])
@login_required
def get_happy_distances( user):
    """Get last user record from cellphone api
    calculate relative distance (in Kilometers) 
    between last user record and fixed locations 
    if user is happy

    Keyword arguments:
    user -- user name
    """
    mood = MoodTypes()
    last_user_record = get_last_user_data(user)
    if not last_user_record:
        return jsonify("User not found"), 404 

    if last_user_record.mood != mood.mood_types['happy']:
        return jsonify("Your user is not happy"), 404 
    else:
        dist_gps = get_location_distances(user)
        try:
            lon, lat= last_user_record.location.split()
            lon, lat = float(lon), float(lat)
        except ValueError:
            return jsonify("GPS coordinates are wrong"), 400
        response = {}
        dist_km = Haversine()
        for item in dist_gps:
            response[item] = dist_km.calculations(dist_gps[item], lat, lon)
        if not response:
            return jsonify("Distances couldn't be found"), 404 
        return jsonify(response), 200 

@views.route('/curr_mood/<user>/', methods=['GET'])
@login_required
def get_current_mood_and_location(user):
    """Get current mood and location from cellphone api
    Check if mood is included in mood type list
    Update/Save in DB location name if exists in response

    Keyword arguments:
    user -- user name
    """   
    if not user:
        return jsonify("User not found"), 404
    if request.method == 'GET':
        res = get_last_user_data(user)
        if not res:
            return jsonify("User not found"), 404 
        else:
            res = {"user_name":res.user_name,"location":res.location,"registered_name_location":res.location_name,"mood":res.mood}
            return jsonify(res), 200     

@views.route('/curr_mood/', methods=['GET','POST'])
def get_current():
    """Get cellphone simulated data and insert in Mood data table
    user name, location, location name and mood
    """   
    if request.method == 'POST':
        user_name = request.values.get("user_name")
        location = request.values.get("location")
        location_name = request.values.get("location_name")
        mood = request.values.get("mood")
        
        if get_api_cell_response(user_name, location, mood, location_name) == ReturnStatus.ERROR:
            return  jsonify("Data is wrong"), 404 
        else:
            return redirect("/", 200)
    return render_template("curr_user.html", user=current_user)

     