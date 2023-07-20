import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import User
# email 인증 관련
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
# 로그인 & 이메일 인증관련
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "email",
            "nickname",
        )
        read_only_fields = ("id", )

    def validate_email(self, obj):
        if User.email_isvalid(obj):
            return obj
        raise serializers.ValidationError('메일 형식이 올바르지 않습니다.')
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        plaintext = '...'
        html_content = render_to_string('users/user_activate_email.html', {
            'user': user,
            'nickname': user.nickname,
            'domain': 'api.kahluabe.co.kr',
            'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': jwt_token,
        })
        mail_subject = '[KAHLUA] 회원가입 인증 메일입니다.'
        to_email = user.email
        from_email = 'hcbkahlua@gmail.com'
        msg = EmailMultiAlternatives(
            mail_subject, plaintext, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        #TODO: 깔루아 로고 이미지 추가
        # msg.attach(image)
        msg.send()
        return user
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'nickname',
        )

    def validate(self, data):
        #email, password에 일치하는 user가 있는지 확인
        email = data.get("email", None)
        password = data.get("password", None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError("아이디 또는 비밀번호를 잘못 입력했습니다.")
            
        else:
            raise serializers.ValidationError("존재하지 않는 email입니다.")
        
        token = RefreshToken.for_user(user=user)
        data = {
            'email': user.email,
            'refresh': str(token),
            'access': str(token.access_token),
            'nickname': user.nickname
        }
        return data