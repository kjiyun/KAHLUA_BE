from django.urls import path
from .views import TicketPurchaseView

app_name = 'tickets'

urlpatterns = [
    path('buy_ticket/', TicketPurchaseView.as_view({'post':'post'}), name='buy_ticket'),
]