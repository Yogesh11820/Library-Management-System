import pytest
from app import app
@pytest.fixture()
def app_test():
    app_test = app
   
    # other setup can go here

    return app_test 

    # clean up / reset resources here


@pytest.fixture()
def client(app_test):
    return app_test.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
