# Generated by Django 4.1.6 on 2023-02-08 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_bankaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='phone_no_with_ext',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
