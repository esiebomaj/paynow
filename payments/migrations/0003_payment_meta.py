# Generated by Django 4.1.6 on 2023-02-06 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_amount_payment_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='meta',
            field=models.JSONField(default=dict),
        ),
    ]
