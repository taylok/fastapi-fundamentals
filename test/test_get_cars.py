from fastapi.testclient import TestClient

from carsharing import app

client = TestClient(app)


# We get a json response, so response.json() which turns the text from the response into actual
# python dicts and lists
def test_get_cars():
    response = client.get("/api/cars/")
    assert response.status_code == 200
    cars = response.json()
    assert all(["doors" in c for c in cars])
    assert all(["size" in c for c in cars])
