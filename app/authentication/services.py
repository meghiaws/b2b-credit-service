from django.db import transaction

from app.core.models import BaseUser
from app.credits.models import Customer, Organization


class AuthenticationService:
    @staticmethod
    def organization_sign_up(
        *, email: str, password: str, organization_name: str
    ) -> None:
        with transaction.atomic():
            user = BaseUser.objects.create_user(email=email, password=password)
            return Organization.objects.create(
                user=user,
                name=organization_name,
            )

    @staticmethod
    def customer_sign_up(*, email: str, password: str, phone: str) -> None:
        with transaction.atomic():
            user = BaseUser.objects.create_user(email=email, password=password)
            return Customer.objects.create(user=user, phone=phone)
