from django.shortcuts import render
from functools import partial

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Ticketing
from .serializers import TicketDetailSerializer

#serializer에 partial=True를 주기위한 Mixin
class SetPartialMixin:
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super().get_serializer_class(*args, **kwargs)
        return partial(serializer_class, partial=True)


class TicketPurchaseView(viewsets.ModelViewSet):
    '''
        티켓 구매 관련 정보를 가져오는 API
    '''
    queryset = Ticketing.objects.all()
    serializer_class = TicketDetailSerializer
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_id='티켓 구매 관련 정보 입력',
        operation_description='''
            티켓을 구매하는 사람이 구매자 이름, 전화번호, 예매인원 등의 정보를 입력합니다.<br/>
            예매 금액을 책정해서 iamport에 넘겨주어야 함</br>
        ''',
    )
    def post(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': 'success',
        }, status=status.HTTP_200_OK)
    

# 구매자 정보 조회는 로그인 시에만 가능
