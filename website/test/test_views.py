import json
import pytest
from website.models import User
from website.views import get_current

@pytest.mark.parametrize(('user', 'status'), (
                         ('romi', 200),
                         ('', 404),
                        ))
def test_get_mood_frequency(client, user, status, views):
    """Test valid user and invalid user to get mood frequency distribution
    """
    views.insert_mood()
    path = "/mood_freq/{}/".format(user)
    response = client.get(path)
    views.clean_mood()
    assert response.status_code == status

@pytest.mark.parametrize(('user', 'mood','status'), (
                         ('romi', 'happy' ,200),
                         ('romi', 'sad' ,404),
                         ('', '',404),
                        ))
def test_get_happy_distances(client, user, mood,status, views):
    """Test valid user and invalid user to get happy relative distances
    """
    views.insert_mood(user_name='romi', location= '-64.6037232 -58.3815931',location_name='school', mood=mood )
    views.insert_fixed_loc(user_name='romi', location= '-64.6037232 -58.3815931',location_name='school')
    path = "/happy_dist/{}/".format(user)
    response = client.get(path)
    views.clean_mood()
    views.clean_fixed_loc()
    assert response.status_code == status

@pytest.mark.parametrize(('user','status'), (
                         ('romi',  200),
                         ('_',  404),
                        ))
def test_get_current_mood_and_location(client, user, status, views):
    """Test location distances of stored locations for a given user
    """
    path = '/curr_mood/{}/'.format(user)
    views.insert_mood()
    response = client.get(path)
    views.clean_mood()
    assert response.status_code == status

@pytest.mark.parametrize(('user', 'location_name','location','mood','status'), (
                         ('', '', '','' , 404),
                         ('', '', 'zapato','' , 404),
                         ('romi', 'disney', '-34.6037232 -58.3815931','happy' , 200),
                        ))
def test_get_current(client, user, location_name,location,mood,status, views):
    """Test location distances of stored locations for a given user
    """  
    views.insert_mood(user_name='romi', location= '-34.6037232 -58.3815931', location_name='disney',mood='happy')
    path = '/curr_mood/?user_name={}&location={}&location_name{}&mood={}'.format(user,location,location_name,mood )
    response = client.post(path)
    views.clean_mood()
    assert response.status_code == status
    
