from django.db.models import QuerySet
from django.db import transaction

from app.core.models import BaseUser
from app.credits.models import Organization


class AuthenticationService:
    @staticmethod
    def sign_up(
        *, email: str, password: str, phone: str, organization_name: str
    ) -> None:
        with transaction.atomic():
            user = BaseUser.objects.create_user(email=email, password=password)
            return Organization.objects.create(
                user=user, name=organization_name, phone=phone
            )
