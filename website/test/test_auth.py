import pytest
from flask import session

@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('testeado@123.com',"123", b'Incorrect password, try again.'),
    ('1@c.com', "1234567", b'Email does not exist.'),
    ('testeado@123.com','testeado', b'Logged in successfully!'),
))
def test_login(client, authorize, email, password , message):
    assert client.get('/login').status_code == 200
    authorize.insert_data(e_mail=email,psw=password)
    response = authorize.login(email,password)
    if response.status_code != 302:
        assert message in response.data
    else:
        assert response.request.path == '/login'


@pytest.mark.parametrize(('email', 'password1','password2','first_name', 'message'), (
    ('com','1234567','1234567', 'test', b'Email must be greater than 3 characters.'),
    ('romi@c.com', '1234567','1234567', '', b'First name must be greater than 1 character.'),
    ('newemail@123.com','testeado','testeado','test', b'Account created!'),
    ('new2@cat.com','1234567','123457','test', b'Passwords do not match.'),
    ('new@cat.com','123','123','test', b'Password must be at least 7 characters.'),
))

def test_sign_up_validation(client, email, password1, password2 ,first_name, message, authorize):
    authorize.insert_data( e_mail='testeado@123.com' , psw ='testeado', name='test')
    response = authorize.sign_up(email,password1, password2, first_name)
    if response.status_code != 302:
        assert message in response.data
    else:
        assert response.request.path == '/sign_up'

    
