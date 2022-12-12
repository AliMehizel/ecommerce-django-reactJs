from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT,HTTP_201_CREATED
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProductView(APIView):

    def get_object(self,pk):
        try:
            return Product.object.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get (self, request, pk , format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, many=False)
        return (serializer.data)



class ProductsList(APIView):

    def get(self,request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class OrederView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        customer = request.user.customer
        oreder, create = Oreder.objects.get_or_create(customer=customer,complete=False)
        orederItem = oreder.orederitem_set.all()
        serializer = OrederItemSerializer(orederItem, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        customer = request.user.customer
        oreder, create = Oreder.objects.get_or_create(customer=customer,complete=False)
        item = request.data['item']
        item_s = get_object_or_404(Product, name = item)
        orederItem_s = OrederItem.objects.filter(oreder=oreder, product=item_s)
        if orederItem_s.exists():
            orederItem_s.quantity += 1
            
        else:
            OrederItem.objects.create(oreder= oreder, product=item_s)
        
        o_Item = OrederItem.objects.get(oreder=oreder, product=item_s)
        serializer = OrederItemSerializer(o_Item, many=False)
        return Response(serializer.data, status=HTTP_201_CREATED)



##edit oreder updateqte/

class EditOrederView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        customer = request.user.customer
        item = request.data['item']
        action = request.data['action']
        item_s = item_s = get_object_or_404(Product, name = item)
        oreder, create = Oreder.objects.get_or_create(customer=customer,complete=False)
        orederItem_s = OrederItem.objects.get(oreder=oreder, product=item_s)
        
        if action == 'add':
            orederItem_s.quantity += 1
        elif action == 'remove':
            orederItem_s.quantity -= 1
        orederItem_s.save()
       
        serializer = OrederItemSerializer(orederItem_s, many=False)
        return Response(serializer.data,status=HTTP_201_CREATED)



class DeleteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return OrederItem.objects.get(pk=pk)
        except OrederItem.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        orederItem = self.get_object(pk=pk)
        orederItem.delete()
        
        return Response( status=HTTP_204_NO_CONTENT)



class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, format=None):
        customer =  request.user.customer
        oreders,create = Oreder.objects.get_or_create(customer = customer, complete =False)
        oreders.complete = True
        oreders.save()
        data = request.data
        
        ShippingAddress.objects.create(
                customer = customer,
                oreder = oreders,
                address = data['address'],
                city = data['city'],
                state = data['state'],
                zipcode= data['zipcode']
            ) 
        address = ShippingAddress.objects.all()
        serializer = AddressSerializer(address, many=True)

        return Response(serializer.data, status = HTTP_201_CREATED)
        

       

