# Generated by Django 2.2 on 2020-05-24 12:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0011_auto_20200524_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 26, 12, 10, 12, 882015, tzinfo=utc)),
        ),
    ]
