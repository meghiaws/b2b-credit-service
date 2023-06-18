from decimal import Decimal
from django.db.models import F
from django.db import transaction
from django.contrib.auth import get_user_model

from app.credits.models import Organization, TransferTransaction


User = get_user_model()


class TransferService:
    @staticmethod
    def transfer_credit_by_phone_number(
        *, sender: User, destination_phone: int, amount: Decimal
    ) -> None:
        with transaction.atomic():
            receiver_organization = Organization.objects.select_for_update().get(
                phone=destination_phone
            )

            sender_organization = Organization.objects.select_for_update().get(
                user=sender
            )

            # create transfer balance record for keep track of increased balances
            TransferTransaction.objects.create(
                sender_id=sender_organization.id,
                receiver_id=receiver_organization.id,
                amount=amount,
            )

            # deposit the actual balance from the sender organization
            sender_organization.balance = F("balance") - amount
            sender_organization.save(update_fields=["balance"])

            # update the actual balance of the organization
            receiver_organization.balance = F("balance") + amount
            receiver_organization.save(update_fields=["balance"])