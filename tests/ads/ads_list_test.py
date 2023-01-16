
import pytest

from tests.factories import AdFactory
from ads.serializers import AdListSerializer


@pytest.mark.django_db
def test_list_view(client):
    ads = AdFactory.create_batch(10)

    response = client.get("/ad/")

    assert response.status_code == 200
    assert response.data == AdListSerializer(ads, many=True).data
