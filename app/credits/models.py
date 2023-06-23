from decimal import Decimal

from django.db import models
from django.db.models import Q, F
from django.utils import timezone
from django.conf import settings


class TimeStamp(models.Model):
    created = models.DateTimeField(db_index=True, default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer"
    )
    phone = models.CharField(max_length=11, unique=True)
    credit = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.CheckConstraint(
                name="customer_credit_not_negative", check=Q(credit__gte=0)
            )
        ]


class Organization(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization"
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0.0))

    class Meta:
        ordering = ("id",)
        constraints = [
            models.CheckConstraint(
                name="organization_balance_not_negative", check=Q(balance__gte=0)
            )
        ]

    def withdraw(self, amount):
        self.balance = F("balance") - amount
        self.save(update_fields=["balance"])

    def deposit(self, amount):
        self.balance = F("balance") + amount
        self.save(update_fields=["balance"])

    def __str__(self) -> str:
        return str(self.id)


class IncreaseBalanceTransaction(models.Model):
    receiver = models.OneToOneField(
        Organization,
        on_delete=models.DO_NOTHING,
        related_name="increased_balance_transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("id",)
        verbose_name = "Increase Balance Transaction"
        verbose_name_plural = "Increase Balance Transactions"

    def __str__(self) -> str:
        return str(self.id)


class TransferTransaction(TimeStamp):
    sender = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        related_name="sent_credits_transactions",
    )
    receiver = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        related_name="received_credits_transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("id",)
        verbose_name = "Transfer Transaction"
        verbose_name_plural = "Transfer Transactions"

    def __str__(self) -> str:
        return str(self.id)
