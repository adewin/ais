# Generated by Django 2.2.4 on 2019-08-27 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aisreceiver', '0002_message_valid_position'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]