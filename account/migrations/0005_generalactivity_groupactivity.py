# Generated by Django 3.0.3 on 2020-02-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_groupfinancial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.IntegerField()),
                ('amount', models.FloatField()),
                ('ref_no', models.CharField(max_length=255)),
                ('Desc', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'general_activity',
            },
        ),
        migrations.CreateModel(
            name='GroupActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('member_id', models.IntegerField()),
                ('member_name', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('ref_no', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'group_activity',
            },
        ),
    ]