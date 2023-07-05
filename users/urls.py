from django.urls import path

from users.views import UserLogoutView, MainView

urlpatterns = [
    path('fruit-shop', MainView.as_view(), name='main'),
    path('logout', UserLogoutView.as_view(), name='logout'),

]