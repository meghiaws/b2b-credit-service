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
                "0914000001",
                "0914000002",
                "0914000003",
                "0914000004",
                "0914000005",
                "0914000006",
                "0914000007",
                "0914000008",
                "0914000009",
                "0914000010",
                "0914000011",
                "0914000012",
                "0914000013",
                "0914000014",
                "0914000015",
            )
        )
        amount = random.randrange(start=10, stop=100, step=10)
        data = {
            "organization_id": organization_id,
            "customer_phone": customer_phone,
            "amount": amount,
        }
        self.client.post(f"/api/transfer/", data=data, name="api/transfer/")
