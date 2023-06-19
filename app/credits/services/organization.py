import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import QuerySet, F
from django.contrib.auth import get_user_model

from app.credits.models import IncreaseBalanceTransaction, Organization
from app.credits.exceptions import OneTimeIncreasedBalanceException

logger = logging.getLogger(__name__)

User = get_user_model()


class OrganizationService:
    @staticmethod
    def organization_list(*, filters=None) -> QuerySet[Organization]:
        return Organization.objects.all()

    @staticmethod
    def organization_get(*, organization_id: int, filters=None) -> Organization:
        return Organization.objects.get(id=organization_id)

    @staticmethod
    def organization_update(*, organization_id: int, name: str, phone: str) -> None:
        Organization.objects.filter(id=organization_id).update(name=name, phone=phone)

    @staticmethod
    def organization_delete(*, organization_id: int) -> None:
        Organization.objects.filter(id=organization_id).delete()

    @staticmethod
    def organization_increase_balance(*, user: User, balance: Decimal) -> None:
        organization_id = (
            Organization.objects.filter(user_id=user.id)
            .values_list("id", flat=True)
            .get()
        )

        # check whether the organization has ever charged its account or not
        already_increased_balance = IncreaseBalanceTransaction.objects.filter(
            receiver_id=organization_id
        ).exists()
        if already_increased_balance:
            logger.exception(
                f"The organization {organization_id} has already used its one time chance to charge its account"
            )
            raise OneTimeIncreasedBalanceException(
                {"message": "you have used your one-time chance to charge your account"}
            )

        logger.info("Starting increase balance process.")
        with transaction.atomic():
            # create increase balance record for keep track of increased balances
            logger.info("Creating increase balance transaction.")
            IncreaseBalanceTransaction.objects.create(
                receiver_id=organization_id, amount=balance
            )

            # update the actual balance of the organization
            logger.info(f"Updating balance of organization {organization_id}.")
            Organization.objects.filter(id=organization_id).update(
                balance=F("balance") + balance
            )

        logger.info(f"Increase balance of organization {organization_id} finished.")
