from os import path, remove
from flask_login import login_user
import pytest
from  website.__init__ import create_app, create_database, db
from werkzeug.security import generate_password_hash
from website.models import FixedLocations, User, MoodData
import sqlalchemy as sa
from alembic import op


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client
        print("auth cli:", client)

    def login(self, e_mail, pwd):
        response = self._client.post(
            '/login',
            data={'email': e_mail, 'password': pwd}
        )
        db.session.query(User).delete()
        db.session.commit()
        return response

    def insert_data(self, e_mail='testeado@123.com' , psw ='testeado', name='test'):
        user = User(email=e_mail, password=generate_password_hash(
                psw, method='sha256'), first_name = name)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return user

    def sign_up( self,email,password, password2, name):
        response = self._client.post(
        '/sign_up',
        data={'email': email, 'password1': password,'password2': password2, 'firstName':name}
        )
        db.session.query(User).delete()
        db.session.commit()
        return response

    def logout(self):
        return self._client.get('/logout')

class ViewsActions(object):
    def __init__(self, client):
        self._client = client
        print("view cli:", client)

    def insert_mood(self,user_name='romi',location ='30.999964 13.000084', location_name='home',mood='happy' ):
        mood_data = MoodData(user_name=user_name, location=location, location_name=location_name, mood=mood)
        db.session.add(mood_data)
        db.session.commit()
        return mood_data

    def insert_fixed_loc(self,user_name='romi',location ='30.999964 13.000084', location_name='home' ):
        locations = FixedLocations(user_name=user_name, location=location, location_name=location_name)
        db.session.add(locations)
        db.session.commit()
        return locations

    def clean_mood(self):
        db.session.query(MoodData).delete()
        db.session.commit()

    def clean_fixed_loc(self):
        db.session.query(FixedLocations).delete()
        db.session.commit()

@pytest.fixture
def authorize(client):
    return AuthActions(client)

@pytest.fixture
def views(client):
    return ViewsActions(client)