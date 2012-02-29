import os

os.environ["STATUSQ_CONFIG_MODE"] = "testing" # XXX: hard-codes statusq.NAME
from statusq import app


class Test(object):

    def setup_method(self, method):
        self.client = app.test_client()
        self.host = "http://localhost"

    def test_create_user(self): # XXX: currently requires a live Redis server
        data = { "username": "jdoe", "password": "foo" }

        response = self.client.post("/users", data=data)
        assert response.status_code == 204

        response = self.client.post("/users", data=data)
        assert response.status_code == 409
