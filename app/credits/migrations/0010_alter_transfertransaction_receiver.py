# Generated by Django 4.2.2 on 2023-06-26 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("credits", "0009_remove_organization_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transfertransaction",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="received_credits_transactions",
                to="credits.customer",
            ),
        ),
    ]
