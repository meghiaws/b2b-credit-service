from django.contrib import admin

from .models import IncreaseBalanceTransaction, Organization, TransferTransaction


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "phone",
        "balance",
    )


@admin.register(IncreaseBalanceTransaction)
class IncreaseBalanceTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "receiver",
        "amount",
    )
    list_filter = ("receiver_id",)


@admin.register(TransferTransaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sender",
        "receiver",
        "amount",
    )
    list_filter = ("sender_id", "receiver_id")
