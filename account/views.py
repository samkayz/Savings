from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
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
        "member_name": c_user_first_name + ' ' + c_user_last_name,
        "saving_bal": "0"
    }
    member = SavingsMemberSerializers(data=mem_data)
    if member.is_valid():
        member.save()
    g_f_data = {
        "group_id": g_id,
        "group_bal": "0"
    }
    group_fin = GroupFinancialSerializers(data=g_f_data)
    if group_fin.is_valid():
        group_fin.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request):
    c_user_id = request.user.id
    group_id = request.data.get('group_id')
    c_user_first_name = request.user.first_name
    c_user_last_name = request.user.last_name

    s_member = {
        "group_id": group_id,
        "member_id": c_user_id,
        "member_name": c_user_first_name + ' ' + c_user_last_name
    }
    if SavingsMember.objects.filter(member_id=c_user_id).exists():
        return Response(status=status.HTTP_302_FOUND)
    else:
        savings_member = SavingsMemberSerializers(data=s_member)
        if savings_member.is_valid():
            savings_member.save()
        return Response(savings_member.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def pay(request):
    ref_no = uuid.uuid4().hex[:10].upper()
    c_user_id = request.user.id
    c_user_first_name = request.user.first_name
    c_user_last_name = request.user.last_name
    am = request.data.get('amount')
    g_id = request.data.get('group_id')
    g_bal = GroupFinancial.objects.values('group_bal').get(group_id=g_id)['group_bal']
    m_bal = SavingsMember.objects.values('saving_bal').get(member_id=c_user_id)['saving_bal']
    amount = float(am)
    gb = float(g_bal)
    new = amount + gb
    new2 = m_bal + amount
    print(new2)

    try:
        snippet = GroupFinancial.objects.get(group_id=g_id)
    except GroupFinancial.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        member = SavingsMember.objects.get(member_id=c_user_id)
    except SavingsMember.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    d = {
        "group_bal": new,
        "group_id": g_id
    }

    serializer = GroupFinancialSerializers(snippet, data=d)
    if serializer.is_valid():
        serializer.save()
        # print(serializer.data)

    g_a = {
        "group_id": g_id,
        "member_id": c_user_id,
        "member_name": c_user_first_name + ' ' + c_user_last_name,
        'amount': am,
        "ref_no": ref_no
    }

    group_activity = GroupActivitySerializers(data=g_a)
    if group_activity.is_valid():
        group_activity.save()

    gen_act = {
        "member_id": c_user_id,
        "amount": am,
        "ref_no": ref_no,
        "Desc": "Contribution"
    }
    gen_activity = GeneralActivitySerializers(data=gen_act)
    if gen_activity.is_valid():
        gen_activity.save()

    bal = {
        "saving_bal": new2,
        "member_id": c_user_id
    }

    sav = SavingsMemberSerializers(member, data=bal)
    if sav.is_valid():
        sav.save()
    print(sav.data)
    return Response(serializer.data)
