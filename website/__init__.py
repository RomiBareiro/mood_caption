from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from website.config import ProductionConfig, TestingConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(ProductionConfig)
        db_name = 'database.db'
    else:
        app.config.from_object(TestingConfig)
        db_name = 'database_test.db'
        app.config["ENV"] = 'development'
        app.config["TESTING"] = True
    '''
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        db_name = 'database.db'
     
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        app.config['LOGIN_DISABLED'] = True
        db_name = 'test.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_name)
    '''
    #swagger configs
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT= get_swaggerui_blueprint(SWAGGER_URL,API_URL, config={'app_name': "Mood Caption"} )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app, db_name)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app, db_name):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
        print('Created Database!')
