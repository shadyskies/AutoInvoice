from django.urls import path
from .views import ProductAPIView, ProductBuyView, UpdateOrderAPIView, GenerateInvoiceAPIView

urlpatterns = [
    path('api/product-list/', ProductAPIView.as_view()),
    path('api/product-buy/', ProductBuyView.as_view()),
    path('api/order-update/<uuid:uuid>', UpdateOrderAPIView.as_view()),
    path('api/generate_invoice/<uuid:uuid>', GenerateInvoiceAPIView.as_view()),
]