from .models import Product, Order, ProductOrder


def check_product_exists(name):
    return True if Product.objects.filter(name=name).exists() else False

def check_available(name, quantity):
    return True if Product.objects.filter(name=name, quantity=quantity).exists() else False
