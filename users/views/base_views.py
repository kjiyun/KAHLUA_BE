from functools import partial
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from users.mixins import ApiAuthMixin, ApiAllowAnyMixin
from users.models import User
from users.serializers import UserSerializer, UserLoginSerializer


#serializer에 partial=True를 주기위한 Mixin
class SetPartialMixin:
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super().get_serializer_class(*args, **kwargs)
        return partial(serializer_class, partial=True)


class SignUpView(SetPartialMixin, CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]

    @swagger_auto_schema(
        operation_id='api_users_signup_post',
        operation_description='''
            전달된 필드값을 기반으로 회원가입을 진행합니다.
        ''',
        responses={
            "200": openapi.Response(
                description="OK",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": {"id": 1}
                    }
                }
            ),
            "400": openapi.Response(
                description="Bad Request",
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            'status': 'Success',
        }, status=status.HTTP_200_OK)
    

class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [
        AllowAny,
    ]

    @swagger_auto_schema(
        operation_id='로그인'
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['email'] == 'None':   # email을 입력받지 않은 경우
                return Response({
                    'status': 'error',
                    'message': '이메일을 입력해주세요.',
                    'code': 404,
                }, status=status.HTTP_404_NOT_FOUND)
            response = {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'nickname': serializer.validated_data['nickname']
            }
            return Response({
                'status': 'success',
                'data': response,
            }, status=status.HTTP_200_OK)
    
class UserInfoView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='내정보조회',
    )
    def retrieve(self, request, *args, **kwargs):
        # 현재 로그인한 사용자 정보 가져오기
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)