from fastapi.testclient import TestClient

from carsharing import app

client = TestClient(app)


# Tell client to do a request to the "/" url to simulate http request and run fastapi operation
# This will currently fail in starlette if there is app.middleware for fastapi
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text
