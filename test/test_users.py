import os

os.environ["STATUSQ_CONFIG_MODE"] = "testing" # XXX: hard-codes statusq.NAME
from statusq import app, database


class Test(object):

    def setup_method(self, method):
        # reset database -- TODO: mock database instead?
        db = database.connect(app)
        db.flushall()

        self.client = app.test_client()
        self.host = "http://localhost"

    def test_registration(self):
        data = { "username": "johndoe", "password": "foo" }

        response = self.client.post("/users", data=data)
        assert response.status_code == 204

        response = self.client.post("/users", data=data)
        assert response.status_code == 409

        data = { "username": "janedoe", "password": "foo" }

        response = self.client.post("/users", data=data, headers={
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"
        })
        assert response.status_code == 302
        assert response.location == "%s/login" % self.host
