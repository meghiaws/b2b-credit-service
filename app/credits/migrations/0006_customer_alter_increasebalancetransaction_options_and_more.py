# Generated by Django 4.2.2 on 2023-06-23 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("credits", "0005_alter_increasebalancetransaction_receiver"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(max_length=11, unique=True)),
                ("credit", models.DecimalField(decimal_places=2, max_digits=12)),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.AlterModelOptions(
            name="increasebalancetransaction",
            options={
                "ordering": ("id",),
                "verbose_name": "Increase Balance Transaction",
                "verbose_name_plural": "Increase Balance Transactions",
            },
        ),
        migrations.AlterModelOptions(
            name="organization",
            options={"ordering": ("id",)},
        ),
        migrations.AlterModelOptions(
            name="transfertransaction",
            options={
                "ordering": ("id",),
                "verbose_name": "Transfer Transaction",
                "verbose_name_plural": "Transfer Transactions",
            },
        ),
        migrations.RemoveConstraint(
            model_name="organization",
            name="constraint_balance_not_negative",
        ),
        migrations.AddConstraint(
            model_name="organization",
            constraint=models.CheckConstraint(
                check=models.Q(("balance__gte", 0)),
                name="organization_balance_not_negative",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="customer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="customer",
            constraint=models.CheckConstraint(
                check=models.Q(("credit__gte", 0)), name="customer_credit_not_negative"
            ),
        ),
    ]
