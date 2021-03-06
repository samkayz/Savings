# Generated by Django 3.0.3 on 2020-02-07 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_savingsgroup_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingsMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('member_id', models.IntegerField()),
                ('member_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'savings_member',
            },
        ),
    ]
