from decimal import Decimal
from django.db import transaction
from django.contrib.auth import get_user_model

from app.credits.models import Organization, TransferTransaction
from app.credits.exceptions import (
    NotEnoughCreditsException,
    TransferDestinationNotFound,
    TransferDestinationNotValid,
)


User = get_user_model()


class TransferService:
    @staticmethod
    def transfer_credit_by_phone_number(
        *, sender: User, destination_phone: int, amount: Decimal
    ) -> None:
        # check if there is destination organization with this phone number or not
        destination_exists = Organization.objects.filter(
            phone=destination_phone
        ).exists()
        if not destination_exists:
            raise TransferDestinationNotFound(
                {"message": "there is no organization with provided phone number"}
            )

        with transaction.atomic():
            receiver_organization = Organization.objects.select_for_update().get(
                phone=destination_phone
            )

            sender_organization = Organization.objects.select_for_update().get(
                user=sender
            )

            # check whether sender organization not trying to transfer credit to itself
            if sender_organization.id == receiver_organization.id:
                raise TransferDestinationNotValid(
                    {"message": "you cannot transfer money to yourself"}
                )

            # check if sender organization has enough money to transfer
            if sender_organization.balance < amount:
                raise NotEnoughCreditsException(
                    {"message": "the sender balance is lower than amount"}
                )

            # create transfer balance record for keep track of increased balances
            TransferTransaction.objects.create(
                sender_id=sender_organization.id,
                receiver_id=receiver_organization.id,
                amount=amount,
            )

            # withdraw the actual balance from the sender organization
            sender_organization.withdraw(amount=amount)

            # deposit the actual balance of the organization
            receiver_organization.deposit(amount=amount)
