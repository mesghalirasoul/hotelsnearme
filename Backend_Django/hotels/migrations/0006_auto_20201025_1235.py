# Generated by Django 3.1.2 on 2020-10-25 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_auto_20201025_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='customer_PhoneNumber',
            new_name='customer_phone_number',
        ),
    ]
