from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(verbose_name='phone', max_length=255, unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'email', 'last_name']
    USERNAME_FIELD = 'phone'

    class Meta:
        db_table = 'user'

    def get_username(self):
        return self


class Transactions(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    trans_type = models.IntegerField()
    ref_no = models.CharField(max_length=100)

    class Meta:
        db_table = "transactions"


class SavingsGroup(models.Model):
    group_author_id = models.IntegerField()
    group_name = models.CharField(max_length=255)
    group_author = models.CharField(max_length=255)
    group_code = models.CharField(max_length=255)
    created_date = models.CharField(max_length=255)

    class Meta:
        db_table = "savings_group"


class SavingsMember(models.Model):
    group_id = models.IntegerField()
    member_id = models.IntegerField()
    member_name = models.CharField(max_length=255)
    saving_bal = models.FloatField()

    class Meta:
        db_table = "savings_member"


class GroupFinancial(models.Model):
    group_id = models.IntegerField()
    group_bal = models.FloatField()

    class Meta:
        db_table = "group_financial"


class GroupActivity(models.Model):
    group_id = models.IntegerField()
    member_id = models.IntegerField()
    member_name = models.CharField(max_length=255)
    amount = models.FloatField()
    ref_no = models.CharField(max_length=255)

    class Meta:
        db_table = "group_activity"


class GeneralActivity(models.Model):
    member_id = models.IntegerField()
    amount = models.FloatField()
    ref_no = models.CharField(max_length=255)
    Desc = models.CharField(max_length=255)

    class Meta:
        db_table = "general_activity"




