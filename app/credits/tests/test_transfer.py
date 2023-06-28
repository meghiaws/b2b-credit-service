import random
import pytest

from django.db.models import Sum
from django.contrib.auth import get_user_model

from app.credits.models import Customer, Organization, TransferTransaction
from app.credits.tests.factories import CustomerFactory, OrganizationFactory


User = get_user_model()


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

    def test_transfer_complete(self, api_client):
        organizations = []
        for i in range(3):
            organization = OrganizationFactory()
            organizations.append(organization)
            for i in range(10):
                increase_balance_data = {
                    "organization_id": organization.id,
                    "balance": 20000,
                }
                response = api_client.post(
                    "/api/increase-balance/", increase_balance_data
                )

                assert response.status_code == 200

        customers = []
        for i in range(20):
            customers.append(CustomerFactory())

        for i in range(1000):
            transfer_data = {
                "organization_id": random.choice(organizations).id,
                "customer_phone": random.choice(customers).phone,
                "amount": 20,
            }
            response = api_client.post("/api/transfer/", transfer_data)
            assert response.status_code == 200

        total_balance = Organization.objects.all().aggregate(
            total_balance=Sum("balance")
        )["total_balance"]

        transferred_amount = TransferTransaction.objects.all().aggregate(
            transferred_amount=Sum("amount")
        )["transferred_amount"]

        received_amount = Customer.objects.all().aggregate(
            received_amount=Sum("credit")
        )["received_amount"]

        assert transferred_amount == received_amount == 20000
        assert total_balance == 580000
