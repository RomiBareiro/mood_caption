from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class MoodData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    location_name = db.Column(db.String(150), nullable=True)
    mood =  db.Column(db.String(10), nullable=False)

class FixedLocations(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    location_name = db.Column(db.String(150))

from website.models import FixedLocations, MoodData
from . import db
from sqlalchemy import func

class ReturnStatus():
    OK = True
    ERROR = False

class MoodTypes():
    mood_types = {}
    def __init__(self):
        self.mood_types['happy'] = "happy"
        self.mood_types['neutral'] = "neutral"
        self.mood_types['sad'] = "sad"
  

def mood_frequency(user):
    """Get mood ocurrences for a given user and total of mood ocurrences
    :param user: User name
    """
    totals = {}
    moodTypes  = MoodTypes()
    total_happy_reg = get_total_nr(user, moodTypes.mood_types['happy'])
    total_neutral_reg = get_total_nr(user, moodTypes.mood_types['neutral'])
    total_sad_reg = get_total_nr(user, moodTypes.mood_types['sad'])

    totals["total_registers"] = total_happy_reg + total_neutral_reg + total_sad_reg
    if totals["total_registers"] != 0:
        totals["happy_freq"] = total_happy_reg / totals["total_registers"]
        totals["neutral_freq"] = total_neutral_reg / totals["total_registers"]
        totals["sad_freq"] = total_sad_reg / totals["total_registers"]
    return totals

def get_total_nr( user , mood):
    """Get quantity of mood ocurrencies for a given user
    Keyword arguments:
    user -- user name
    mood -- mood (could be "sad", "happy" or "neutral")
    """
    times = MoodData.query.filter_by(user_name=user , mood=mood).count()
    return times


def get_location_distances(user):
    """Get location distances of stored locations for a given user
    Keyword arguments:
    user -- user name
    """
    dict_res = {}
    if not user:
        return dict_res
    else:
        res = FixedLocations.query.filter_by(user_name=user).all()

        for i in range(0,len(res)):
            dict_res[res[i].location_name] = res[i].location

    return dict_res
   
# It is possible to modify location if location name exists
def update_fixed_table(user, location_name, location):
    """Save or update location name and location for a given user
    Keyword arguments:
    user -- user name
    location_name -- location name to be saved
    location -- location coordinates to be saved
    """
    if (not user) or (not location_name):  
        return ReturnStatus.ERROR
    else:
        res = FixedLocations.query.filter_by(user_name=user , location_name=location_name).all()
        if not res:             #insert
            res = FixedLocations(user_name=user,location_name=location_name, location=location)
            db.session.add(res)
        else:                   #update
            res[0].location = location
            db.session.add(res[0])
        db.session.commit()
    return ReturnStatus.OK
    
def update_mood_table(payload):
    """Save mood and location response in MoodData model
    Keyword arguments:
    moodObject -- Mood() object
    """
    if not payload:
        return ReturnStatus.ERROR

    user = payload["user_name"]
    if not user:
        return ReturnStatus.ERROR
    
    location = payload["location"]
    location_name = payload["registered_name_location"]
    mood = payload["mood"]
    
    res = MoodData( user_name=user,location=location, location_name=location_name, mood=mood )
    db.session.add(res)
    db.session.commit()
    if location_name :
        update_fixed_table( user,location=location, location_name=location_name )
    return ReturnStatus.OK

def get_last_user_data(user):
    """Get last data of a given user
    Keyword arguments:
    user -- user name 
    """
    res = {}
    if not user:
        return res
    res = MoodData.query.filter_by(user_name=user).order_by(MoodData.id.desc()).first()
    return res