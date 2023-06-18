from decimal import Decimal
from django.db import transaction
from django.db.models import QuerySet, F
from django.contrib.auth import get_user_model

from app.credits.models import IncreaseBalanceTransaction, Organization

User = get_user_model()


class OrganizationService:
    @staticmethod
    def organization_list(*, filters=None) -> QuerySet[Organization]:
        return Organization.objects.all()

    @staticmethod
    def organization_get(*, organization_id: int, filters=None) -> Organization:
        return Organization.objects.get(id=organization_id)

    @staticmethod
    def organization_delete(*, organization_id: int) -> None:
        Organization.objects.filter(id=organization_id).delete()

    @staticmethod
    def organization_increase_balance(
        *, user: User,balance: Decimal
    ) -> None:
        organization_id = (
            Organization.objects.filter(user_id=user.id)
            .values_list("id", flat=True)
            .get()
        )
        with transaction.atomic():
            # create increase balance record for keep track of increased balances
            IncreaseBalanceTransaction.objects.create(
                receiver_id=organization_id, amount=balance
            )

            # update the actual balance of the organization
            Organization.objects.filter(id=organization_id).update(
                balance=F("balance") + balance
            )
            
