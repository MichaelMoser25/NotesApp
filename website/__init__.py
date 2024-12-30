# Set up Flask Application
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# define the database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Encrypt data - secret key for the app
    app.config['SECRET_KEY'] = 'ajbvlafbla jbvljadnfdl'

    # sql database is stored at this location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # initialize databse by giving it flask app
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # database
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    # where fo we need to go if not logged in (where should flask redirect if user is not logged in)
    login_manager.login_view = 'auth.login'
    # tell login manager which app we are using
    login_manager.init_app(app)

    # tell flask how to load a user
    @login_manager.user_loader
    def load_user(id):
        # by default look for primary key
        return User.query.get(int(id))


    return app

# check if database exists, if not create it
def create_database(app):
    # determine if path to db exists
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')

