
import random
from django.shortcuts import render

from .producer import publish
from .models import Product, User

from .serializer import ProductSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class ProductViewSet(viewsets.ViewSet):
    def list(self,request):
        products=Product.objects.all() 
        serializer = ProductSerializer(products,many=True)
        # publish()
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created',serializer.data)
        print('product_created')
        return Response(serializer.data,status=status.HTTP_201_CREATED)


    def retrive(self,request,pk=None):
        product=Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self,request,pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated',serializer.data)
        print('product_updated')
        return Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self,request,pk=None):
        product=Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted',pk)
        print('product_deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        print('Akshay',users)
        user = random.choice(users)
        return Response({
            'id':user.id
                    })


