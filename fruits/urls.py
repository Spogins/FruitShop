from django.urls import path

from fruits.views import buy_or_sell_fruits

urlpatterns = [
    path('ajax-buy-or-sell-fruits/', buy_or_sell_fruits, name='buy_or_sell_fruits'),
]