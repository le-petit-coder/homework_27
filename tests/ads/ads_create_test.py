import pytest


@pytest.mark.django_db
def test_create_ad(client, user_token):
    expected_response = {
        "id": 1,
        "name": "test",
        "author": None,
        "price": 0,
        "locations": [],
        "is_published": False
    }

    data = {
        "name": "test",
        "price": 0
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION="Token " + user_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
