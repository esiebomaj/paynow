# Generated by Django 4.1.6 on 2023-02-12 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_payment_created_at_payment_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='payment',
            name='purpose',
            field=models.CharField(choices=[('withdrawal', 'Withdrawal'), ('reverse_withdrawal', 'Reverse Withdrawal'), ('topup', 'Topup'), ('transfer_credit', 'Transfer Credit'), ('transfer_debit', 'Transfer Debit')], max_length=100),
        ),
    ]
