import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import QuerySet, F
from django.contrib.auth import get_user_model

from app.credits.models import IncreaseBalanceTransaction, Organization
from app.credits.exceptions import OneTimeIncreasedBalanceException

logger = logging.getLogger(__name__)

User = get_user_model()


class IncreaseBalanceService:

    @staticmethod
    def increase_balance(
        *, organization_id: int, balance: Decimal
    ) -> None:

        logger.info("Starting increase balance process.")
        with transaction.atomic():
            # organization = Organization.objects.get(id=organization_id)

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
