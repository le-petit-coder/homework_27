import pytest


@pytest.mark.django_db
def test_create_selection(client, user_token):
    expected_response = {
        "id": 1,
        "name": "new selection",
        "owner": 1,
        "items": [1]
    }

    response = client.post("/selection/", data={
            "name": "new selection",
            "owner": 1,
            "items": [1]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + user_token)

    new_list = response.data

    assert new_list == expected_response
    assert response.status_code == 201

