from django.shortcuts import render
from firebase_admin import initialize_app


def login_backend(request):
    return render(request, 'user/login_backend.html') 

def logout_backend(request):
    return render(request, 'user/logout.html')

def ftoken(request):
    return render(request, 'user/ftoken.html')
    