from django.urls import path
from .views import login_backend, logout_backend, ftoken

urlpatterns = [
    path('login/', login_backend),
    path('logout/', logout_backend),
    path('ftoken/', ftoken),
]