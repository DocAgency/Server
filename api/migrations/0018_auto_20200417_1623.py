# Generated by Django 3.0.5 on 2020-04-17 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20200414_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
