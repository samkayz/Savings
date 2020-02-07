from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone')


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('id', 'sender_id', 'receiver_id', 'trans_type', 'ref_no')


class SavingsGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingsGroup
        fields = ('id', 'group_author_id', 'group_name', 'group_author', 'group_code', 'created_date')


class SavingsMemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = SavingsMember
        fields = ('id', 'group_id', 'member_id', 'member_name')
