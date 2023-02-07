# Generated by Django 4.1.6 on 2023-02-06 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_payment_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='external_access_code',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='external_authorization_url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
