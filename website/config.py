class DbConfig(object):
    database = "database"
    engine = 'sqlite:///'
    SQLALCHEMY_BINDS = {
        'db': engine + database + '.db',
        'db2': engine + database + '_test.db' 
    }
    SECRET_KEY = 'hjshjhdjah kjshkjdhjs'

class TestingConfig(DbConfig):
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = DbConfig.engine  + DbConfig.database + '_test.db'

    # your config for testing environment

class ProductionConfig(DbConfig):
    # your config for production environment
    SQLALCHEMY_DATABASE_URI = DbConfig.engine + 'database.db'


   
    