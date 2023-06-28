from random import randint
import random
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(2, 5)

    def on_start(self):
        ...

    @task(1)
    def increase_income(self):
        organization_id = random.randint(1, 5)
        balance =  random.randrange(start=50, stop=300, step=50)
        data = {"organization_id": organization_id, "balance": balance}
        self.client.post(
            f"/api/increase-balance/", data=data, name="api/increase-balance/"
        )

    @task(3)
    def transfer(self):
        organization_id = random.randint(1, 5)
        customer_phone = random.choice(
            (
                "09140000001",
                "09140000002",
                "09140000003",
                "09140000004",
                "09140000005",
                "09140000006",
                "09140000007",
                "09140000008",
                "09140000009",
                "09140000010",
                "09140000011",
                "09140000012",
            )
        )
        amount = random.randrange(start=10, stop=100, step=10)
        data = {
            "organization_id": organization_id,
            "customer_phone": customer_phone,
            "amount": amount,
        }
        self.client.post(f"/api/transfer/", data=data, name="api/transfer/")
