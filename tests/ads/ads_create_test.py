import pytest


@pytest.mark.django_db
def test_create_ad(client, user_token):
    expected_response = {
        "id": 1,
        "name": "new advertise",
        "author": None,
        "price": 10,
        "locations": [],
        "is_published": False
    }

    response = client.post("/ad/create/", data={
        "name": "new advertise",
        "price": 10
    }, content_type="application/json", HTTP_AUTHORIZATION="Token " + user_token)

    assert response.status_code == 201
    assert response.data == expected_response
