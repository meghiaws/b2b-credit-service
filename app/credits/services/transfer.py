import logging
from decimal import Decimal

from django.db import transaction
from django.contrib.auth import get_user_model

from app.credits.models import Customer, Organization, TransferTransaction
from app.credits.exceptions import (
    NotEnoughCreditsException,
    TransferDestinationNotFound,
    TransferDestinationNotValid,
)

logger = logging.getLogger(__name__)

User = get_user_model()


class TransferService:
    @staticmethod
    def transfer_credit_by_phone_number(
        *, organization_id: int, customer_phone: int, amount: Decimal
    ) -> None:
        # check if there is destination organization with this phone number or not
        destination_exists = Customer.objects.filter(
            phone=customer_phone
        ).exists()
        if not destination_exists:
            logger.exception(
                f"There is no customer with {customer_phone} phone number."
            )
            raise TransferDestinationNotFound(
                {"message": "there is no customer with provided phone number"}
            )

        logger.info("Starting the credit transfer process.")
        with transaction.atomic():
            customer = Customer.objects.select_for_update().get(
                phone=customer_phone
            )

            organization = Organization.objects.select_for_update().get(
                id=organization_id
            )

            # check if sender organization has enough money to transfer
            if organization.balance < amount:
                logger.exception(
                    f"Sender balance ({organization.balance}) is lower than transfer amount ({amount})."
                )
                raise NotEnoughCreditsException(
                    {"message": "the sender balance is lower than amount"}
                )

            # create transfer balance record for keep track of increased balances
            logger.info("Creating record for transfer transactions.")
            TransferTransaction.objects.create(
                organization_id=organization.id,
                customer_id=customer.id,
                amount=amount,
            )

            # withdraw the actual balance from the sender organization
            logger.info(
                f"Withdrawing credits from organization {organization.name}."
            )
            organization.withdraw(amount=amount)

            # deposit the actual balance of the organization
            logger.info(
                f"Depositing credits to user with phone number {customer_phone}."
            )
            customer.deposit(amount=amount)

        logger.info(
            f"Transferring credits from {organization.name} to phone number {customer_phone} finished."
        )
