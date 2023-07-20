from django.db import models
from core.models import TimeStampedModel

class Category(models.Model):
    name = models.CharField(max_length=30)   # 티켓 종류 구분 (일반/신입생)

    def __str__(self):
        return self.name

class Ticketing(TimeStampedModel):
    category = models.ForeignKey('Category', related_name='tickets', on_delete=models.CASCADE)
    buyer = models.CharField(max_length=20)   # 결제자 이름
    phone_num = models.CharField(max_length=20)   # 핸드폰 번호
    email = models.CharField(max_length=50)
    member = models.PositiveIntegerField(default=1)   # 결제 인원
    available_ticket = models.BooleanField(default=True)   # 티켓 구매 가능 여부
    meeting = models.BooleanField(default=False)   # 소모임 참석 가능 여부 확인

    def __str__(self):
        return self.buyer
    