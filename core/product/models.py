from django.db import models
import uuid


class Order(models.Model):
    invoice_id = models.UUIDField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=1024)
    individual_product_order = models.ManyToManyField('product.Product', through='product.ProductOrder', null=True)
    total = models.FloatField()
    invoice_file = models.FileField(upload_to='invoice_pdf')

    def __str__(self):
        return f"{self.invoice_id} --> {self.customer}"
    

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, null=True)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name
        

# intermediary model b/w order and product
class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.order} --> {self.product.name}"