import random

from flask import Flask

# injected models
from models.base import db
from models import *
from _johndatabase import delete_all_data, populate_database
# routes endpoints
from routes.project_routes import project_endpoints
from routes.user_routes import users_bp

from routes.task_routes import task_endpoints
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


with app.app_context():
    print("creating db")
    db.create_all()
    delete_all_data(db)
    populate_database("hf://datasets/JohnVans123/ProjectManagement/Project Management (2).csv",db)

app.register_blueprint(users_bp)
app.register_blueprint(project_endpoints)
app.register_blueprint(task_endpoints)

if __name__ == "__main__":
    app.run(debug=True)
