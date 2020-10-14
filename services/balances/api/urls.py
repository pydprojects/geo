from django.urls import path
from . import views


urlpatterns = [
    path("balances/", views.Balances.as_view(), name='balances'),
    path("balances/<int:user_id>", views.UserBalance.as_view(), name='user_balance')
]
