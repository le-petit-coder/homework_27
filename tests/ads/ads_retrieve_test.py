import pytest


@pytest.mark.django_db
def test_retrieve_test(client, ad, user_token):
    expected_response = {
        "id": ad.pk,
        "name": ad.name,
        "author": ad.author,
        "price": ad.price,
    }

    response = client.get(f"/ad/{ad.pk}/",
                          content_type='application/json',
                          HTTP_AUTHORIZATION="Bearer " + user_token
                          )

    assert response.status_code == 200
    assert response.data == expected_response
