#\Group_06_Bernacchia_Fernandez\backend> pipenv run pytest tests/

import pytest
import sys
import os
# TODO: should be more clean change all the import inside the app,
#       but in this way the app won't be "independent"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from _johndatabase import populate_database,delete_all_data
from app import app, db

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # DB temp in RAM
    with app.app_context():
        db.create_all()
        delete_all_data(db)
        populate_database(r".\tests\data_test.csv", db)
        yield app.test_client()
        db.session.remove()
        db.drop_all()