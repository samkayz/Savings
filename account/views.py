from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
import requests
from datetime import datetime
import random
import string
import uuid
from .models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
    return Response(data="Only for Login User", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money(request):
    c_user_id = request.user.id
    r_id = request.data.get('email')
    amount = request.data.get('amount')
    rec_id = User.objects.values('id').get(email=r_id)['id']
    r_bal = User.objects.values('bal').get(email=r_id)['bal']
    rb = (float(r_bal))
    am = (float(amount))
    new = rb + am
    new_bal = {
        "bal": new
    }
    data_attr = {
        "sender_id": c_user_id,
        "receiver_id": rec_id,
        "trans_type": '1',
        "ref_no": "Earsf"
    }
    balance = UserCreateSerializer(User, data=new_bal)
    if balance.is_valid():
        balance.save()
    serializer = TransactionSerializers(data=data_attr)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    N = 5
    res = ''.join(random.choices(string.digits, k=N))
    g_code = str(res)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
    c_user_id = request.user.id
    c_user_first_name = request.user.first_name
    c_user_last_name = request.user.last_name
    g_name = request.data.get('group_name')

    create_data = {
        "group_author_id": c_user_id,
        "group_name": g_name,
        "group_author": c_user_first_name + ' ' + c_user_last_name,
        "group_code": g_code,
        "created_date": date
    }
    serializer = SavingsGroupSerializers(data=create_data)
    if serializer.is_valid():
        serializer.save()

    g_id = SavingsGroup.objects.values('id').get(group_name=g_name)['id']
    mem_data = {
        "group_id": g_id,
        "member_id": c_user_id,
        "member_name": c_user_first_name + ' ' + c_user_last_name
    }
    member = SavingsMemberSerializers(data=mem_data)
    if member.is_valid():
        member.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
