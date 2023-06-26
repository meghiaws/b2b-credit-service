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
        *, sender_user: User, customer_phone: int, amount: Decimal
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
                {"message": "there is no organization with provided phone number"}
            )

        logger.info("Starting the credit transfer process.")
        with transaction.atomic():
            receiver = Customer.objects.select_for_update().get(
                phone=customer_phone
            )

            sender = Organization.objects.select_for_update().get(
                user=sender_user
            )

            # check whether sender organization not trying to transfer credit to itself
            # if sender.id == receiver_organization.id:
            #     logger.exception(
            #         f"Cannot transfer money from {sender_organization.id} to {receiver_organization.id}."
            #     )
            #     raise TransferDestinationNotValid(
            #         {"message": "you cannot transfer money to yourself"}
            #     )

            # check if sender organization has enough money to transfer
            if sender.balance < amount:
                logger.exception(
                    f"Sender balance ({sender.balance}) is lower than transfer amount ({amount})."
                )
                raise NotEnoughCreditsException(
                    {"message": "the sender balance is lower than amount"}
                )

            # create transfer balance record for keep track of increased balances
            logger.info("Creating record for transfer transactions.")
            TransferTransaction.objects.create(
                sender_id=sender.id,
                receiver_id=receiver.id,
                amount=amount,
            )

            # withdraw the actual balance from the sender organization
            logger.info(
                f"Withdrawing credits from organization {sender.name}."
            )
            sender.withdraw(amount=amount)

            # deposit the actual balance of the organization
            logger.info(
                f"Depositing credits to organization {receiver.name}."
            )
            receiver.deposit(amount=amount)

        logger.info(
            f"Transferring credits from {sender.name} to organization {receiver.name} finished."
        )
