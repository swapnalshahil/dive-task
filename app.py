from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from models import db
import sqlite3
from models.user import User

from routes.auth import auth_bp
from routes.entry import entry_bp
from routes.user import users_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['FLASK_DEBUG'] = app.config['DEBUG']

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)



# Register the blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(entry_bp)
app.register_blueprint(users_bp)

login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Connect to the database
    conn = sqlite3.connect('database.db')
    print("Connected to the database successfully")

    # Close the database connection
    conn.close()

    app.run()
