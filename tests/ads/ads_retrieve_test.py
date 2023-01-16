import pytest


@pytest.mark.django_db
def test_retrieve_test(client, ad, user_token):
    expected_response = {
        "id": ad.pk,
        "author": ad.author,
        "price": ad.price,
        "description": ad.description,
        "address": ad.address,
        "is_published": ad.is_published,
        "image": ad.image,
        "category": ad.category,
        "locations": ad.locations
    }

    response = client.get(f"/ad/{ad.pk}/",
                          content_type='application/json',
                          HTTP_AUTHORIZATION="Token " + user_token
                          )

    assert response.status_code == 200
    assert response.data == expected_response
