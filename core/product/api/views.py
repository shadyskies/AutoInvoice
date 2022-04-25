from math import prod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Product, Order, ProductOrder
from .serializers import GenerateInvoiceSerializer, ProductSerializer, ProductBuySerializer
from ..utils import check_product_exists, check_available
# from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from pathlib import Path
import sys


class ProductAPIView(APIView):
    '''
    Return the details of available items
    '''

    def get(self, request, *args, **kwargs):
        qs = Product.objects.filter(quantity__gt=0).order_by('name')
        data = ProductSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ProductBuyView(APIView):
    '''
    Create order of what user is buying 
    '''
    serializer_class = ProductBuySerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # check if received data is in required form
        ser = ProductBuySerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.data
        # if multiple same items in request
        if len(set(data)) != len(data):
            return Response('Products repeated', status=status.HTTP_400_BAD_REQUEST)

        # if the products and quantity are not same length
        if len(data['product'])!=len(data['quantity']):
            return Response('Product and Quantity mismatch', status=status.HTTP_400_BAD_REQUEST)
        
        total = 0
        products = data['product']
        quantity = data['quantity']
        objs = []
        product_objs_ls = []
        # create an order to associate with individual product orders
        order_obj = Order.objects.create(total=0, customer=request.user)

        for i in range(len(products)):
            prod_obj = Product.objects.filter(name=products[i])
            # product not exists
            if not prod_obj:
                order_obj.delete()
                return Response('Product not found', status=status.HTTP_400_BAD_REQUEST)
            # quantity greater than available quantity
            prod_obj = prod_obj.first()
            if prod_obj.quantity < quantity[i]:
                order_obj.delete()
                return Response('Quantity greater than available quantity', status=status.HTTP_400_BAD_REQUEST)
            
            # create product_order
            product_order = ProductOrder(product=prod_obj, quantity=quantity[i], order=order_obj)
            total += quantity[i] * prod_obj.price
            prod_obj.quantity -= quantity[i]
            objs.append(prod_obj)
            objs.append(product_order)
            product_objs_ls.append(prod_obj)

        # complete order creation if necessary condtions met
        for i in objs:
            i.save()
        order_obj.total=total
        
        # add individual product orders to Order
        for i in product_objs_ls:
            order_obj.individual_product_order.add(i)
        
        order_obj.save()
        return Response(status=status.HTTP_201_CREATED)


class UpdateOrderAPIView(APIView):
    '''
    Updates the order based on uuid 
    '''
    serializer_class = ProductBuySerializer
    permission_classes = (IsAuthenticated, )
    
    def put(self, request, uuid):
        # check if order exists
        print(f"uuid: {uuid}")
        order_obj = Order.objects.filter(invoice_id=uuid)
        print(f"order_obj: {order_obj}")
        if not order_obj:
            return Response("Order does not exist", status=status.HTTP_404_NOT_FOUND)
        order_obj = order_obj.first()

        ser = ProductBuySerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.data
        # if multiple same items in request
        if len(set(data)) != len(data):
            return Response('Products repeated', status=status.HTTP_400_BAD_REQUEST)

        # if the products and quantity are not same length
        if len(data['product'])!=len(data['quantity']):
            return Response('Product and Quantity mismatch', status=status.HTTP_400_BAD_REQUEST)
        
        total = 0
        products = data['product']
        quantity = data['quantity']
        objs = []
        product_objs_ls = []
        
        # check if exists and avai;able first
        for i in range(len(products)):
            prod_obj = Product.objects.filter(name=products[i])
            # product not exists
            if not prod_obj:
                return Response('Product not found', status=status.HTTP_400_BAD_REQUEST)
            # quantity greater than available quantity
            prod_obj = prod_obj.first()
            if prod_obj.quantity < quantity[i]:
                return Response('Quantity greater than available quantity', status=status.HTTP_400_BAD_REQUEST)
            
        for i in range(len(products)):
            prod_obj = Product.objects.filter(name=products[i])
            prod_obj = prod_obj.first()

            # check if product exists in order
            qs = ProductOrder.objects.filter(order=order_obj, product=prod_obj)
            # update the quantity in order
            if qs:
                tmp_obj = qs.first()
                print(tmp_obj.__dict__)
                tmp_obj.quantity +=  quantity[i]
                print(tmp_obj.__dict__)
                tmp_obj.save()
                objs.append(qs.first())
                
            # create the new product order
            else:
                obj = ProductOrder(order=order_obj, quantity=quantity[i], product=prod_obj.first())
                objs.append(obj)
                product_objs_ls.append(prod_obj.first())

            total += quantity[i] * prod_obj.price
            prod_obj.quantity -= quantity[i]
            objs.append(prod_obj)

        # save all the product orders 
        for i in objs: 
            print(f"obj: {i}")
            i.save()

        order_obj.total += total
        # associate the new product orders with order 
        for i in product_objs_ls:
            order_obj.individual_product_order.add(i)
        
        order_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
            

class GenerateInvoiceAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = GenerateInvoiceSerializer
    '''
    Dynamically generate invoice based on details 
    '''

    def get(self, request, uuid):
        order_obj = Order.objects.filter(invoice_id=uuid)
        if not order_obj:
            return Response("Order not found", status=status.HTTP_400_BAD_REQUEST)
        order_obj = order_obj.first()

        # if details are not sent
        ser = GenerateInvoiceSerializer(request.GET)
        if not ser.is_valid:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.data
        print(data['address'])
        print(f"individual_prods: {order_obj.individual_product_order.first().__dict__}")

        # getting the template to convert to pdf
        template_path = "product/invoice_template.html"
        context = {
            "customer_name": data['customer_name'],
            "phone": data['phone'],
            "address": data['address'],
            "order_prods": ProductOrder.objects.filter(order=order_obj),
            "order_total": order_obj.total
        }
        template = get_template(template_path)
        html = template.render(context)
        outfile = f'invoice_pdf/{order_obj.invoice_id}.pdf'

        # # open output file for writing (truncated binary)
        # result_file = open(f'{order_obj.invoice_id}.pdf', "w+b")

        # # convert HTML to PDF
        # pisa_status = pisa.CreatePDF(
        #         html,                # the HTML to convert
        #         dest=result_file)           # file handle to recieve result

        # # close output file
        # result_file.close()                 # close output file

        # if pisa_status.err:
        #     return Response("pdf generation failed",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        htmldoc = HTML(string=html, base_url="")
        Path(outfile).write_bytes(htmldoc.write_pdf())

    
        order_obj.invoice_file = f'invoice_pdf/{order_obj.invoice_id}.pdf'
        order_obj.phone = data['phone']
        order_obj.address = data['address']
        order_obj.save()


        return Response(order_obj.invoice_file.url, status=status.HTTP_200_OK)
        