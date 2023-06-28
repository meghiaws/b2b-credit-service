import pytest

from django.contrib.auth import get_user_model

from app.credits.models import Customer, Organization, TransferTransaction
from app.credits.tests.factories import CustomerFactory, OrganizationFactory


User = get_user_model()


@pytest.fixture
def organization_with_zero_balance():
    user = User.objects.create_user(email="email1@domain.com", password="12345")
    return Organization.objects.create(user=user, name="organization_test_1")


@pytest.fixture
def organization_with_positive_balance():
    user = User.objects.create_user(email="email2@domain.com", password="12345")
    return Organization.objects.create(
        user=user, name="organization_test_2", balance=200
    )


@pytest.fixture
def customer():
    user = User.objects.create_user(email="email@domain.com", password="12345")
    return Customer.objects.create(user=user, phone="09140000000")


@pytest.mark.django_db(reset_sequences=True)
class TestTransfer:
    def test_transfer_to_invalid_phone(self, api_client):
        organization = OrganizationFactory()
        data = {
            "organization_id": organization.id,
            "customer_phone": "09140000006",
            "amount": 100,
        }
        response = api_client.post("/api/transfer/", data)

        assert response.status_code == 404

    def test_transfer_with_balance_less_than_amount(self, api_client):
        organization = OrganizationFactory()
        customer = CustomerFactory()
        data = {
            "organization_id": organization.id,
            "customer_phone": customer.phone,
            "amount": 100,
        }
        response = api_client.post("/api/transfer/", data)

        assert response.status_code == 400

    def test_transfer_with_not_enough_balance(self, api_client):
        organization = OrganizationFactory()
        customer = CustomerFactory()
        data = {
            "organization_id": organization.id,
            "customer_phone": customer.phone,
            "amount": 100,
        }
        response = api_client.post("/api/transfer/", data)

        assert response.status_code == 400

    def test_transfer_with_enough_balance(self, api_client):
        organization = OrganizationFactory(balance=200)
        customer = CustomerFactory()
        data = {
            "organization_id": organization.id,
            "customer_phone": customer.phone,
            "amount": 50,
        }
        response = api_client.post("/api/transfer/", data)

        customer.refresh_from_db()
        organization.refresh_from_db()

        transaction = TransferTransaction.objects.get(
            organization=organization, customer=customer
        )
        assert response.status_code == 200
        assert transaction.amount == 50
        assert customer.credit == 50
        assert organization.balance == 150
