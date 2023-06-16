from decimal import Decimal
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings


class TimeStamp(models.Model):
    created = models.DateTimeField(db_index=True, default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization"
    )
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0))

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="constraint_balance_not_negative", check=Q(balance__gte=0)
            )
        ]

    def __str__(self) -> str:
        return str(self.id)


class IncreaseBalanceTransaction(models.Model):
    receiver = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        related_name="increased_balance_transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return str(self.id)


class TransferTransaction(TimeStamp):
    sender = models.ForeignKey(
        Organization, on_delete=models.DO_NOTHING, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        Organization, on_delete=models.DO_NOTHING, related_name="received_transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return str(self.id)
