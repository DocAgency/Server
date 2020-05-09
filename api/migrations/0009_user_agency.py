# Generated by Django 3.0.5 on 2020-04-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_indicator_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='agency',
            field=models.ManyToManyField(through='api.UserAgency', to='api.Agency'),
        ),
    ]
