# Generated by Django 3.0.3 on 2020-02-08 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_generalactivity_groupactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsmember',
            name='saving_bal',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
