from django.db import models
import uuid


class Invoice(models.Model):
    invoice_id = models.UUIDField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=1024)
    total = models.FloatField()
    invoice_file = models.FileField(upload_to='invoice_pdf')

    def __str__(self):
        return f"{self.invoice_id} --> {self.customer}"

class Product(models.Model):
    name = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name