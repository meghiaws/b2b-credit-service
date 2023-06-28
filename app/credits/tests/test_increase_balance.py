import pytest

from django.contrib.auth import get_user_model

from app.credits.tests.factories import OrganizationFactory


User = get_user_model()


@pytest.mark.django_db(reset_sequences=True)
class TestIncreaseBalance:
    def test_increase_balance_with_negative_amount(self, api_client):
        organization = OrganizationFactory()
        data = {"organization_id": organization.id, "balance": -10}
        response = api_client.post("/api/increase-balance/", data)

        assert response.status_code == 400

    def test_increase_balance_with_three_decimal_places(self, api_client):
        organization = OrganizationFactory()
        data = {"organization_id": organization.id, "balance": 0.001}
        response = api_client.post("/api/increase-balance/", data)

        assert response.status_code == 400

    def test_increase_balance_with_lowest_possible_balance(self, api_client):
        organization = OrganizationFactory()
        data = {"organization_id": organization.id, "balance": 0.01}
        response = api_client.post("/api/increase-balance/", data)

        assert response.status_code == 200

    def test_increase_balance_with_normal_amount(self, api_client):
        organization = OrganizationFactory()
        data = {"organization_id": organization.id, "balance": 100}
        response = api_client.post("/api/increase-balance/", data)

        assert response.status_code == 200
