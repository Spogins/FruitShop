from django.urls import path

from bank.views import update_bank_account

urlpatterns = [
    path('ajax-top-up-account/', update_bank_account, name='update_bank_account'),
]