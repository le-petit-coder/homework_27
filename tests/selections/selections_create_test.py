import pytest


@pytest.mark.django_db
def test_create_selection(client, user_token):
    expected_response = {
        "id": 1,
        "name": "test",
        "owner": None,
        "items": []
    }

    data = {
        "name": "test",
        "items": []
    }

    response = client.post(
        "/selection/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION="Token " + user_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
