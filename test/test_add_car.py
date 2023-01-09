from unittest.mock import Mock

from fastapi.testclient import TestClient
from fastapi import Response

from carsharing import app
from routers.cars import add_car
from schemas import CarInput, User, Car

client = TestClient(app)


# def test_add_car():
#     response = client.post("/api/cars/",
#                            json={
#                                "doors": 7,
#                                "size": "xl",
#                            }, headers={'Authorisation': 'Bearer taylok'}
#                            )
#     assert response.status_code == 200
#     car = response.json()
#     assert car["doors"] == 7
#     assert car["size"] == 'xxl'


# mock object from built-in library
def test_add_car_with_mock_session():
    mock_session = Mock()
    input = CarInput(doors=2, size="xl")
    user = User(username="taylok")
    result = add_car(car_input=input, session=mock_session, user=user, response=Response)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Car)
    assert result.doors == 2
    assert result.size == "xl"
