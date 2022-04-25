import firebase_admin
from rest_framework.authentication import BaseAuthentication
from .exceptions import *
from firebase_admin import auth
from django.conf import settings
from user.models import CustomUser

if not firebase_admin._apps:
                firebase_admin.initialize_app()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # print(request.META)
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        # print(auth_header)
        if not auth_header:
            return None
        id_token = auth_header.split(" ").pop()
        # print(f"id_token: {id_token}")
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e)
        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user, created = CustomUser.objects.get_or_create(email=decoded_token.get("email"), firebase_id=uid)
        print(f"user: {user}")
        return (user, None)