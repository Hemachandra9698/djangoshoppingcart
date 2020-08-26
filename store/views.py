from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import utils


class Store(APIView):
    def get(self, request):
        context = utils.get_items_orders_and_cart_items(request)
        products = utils.get_all_products()
        context['products'] = products
        return render(request, 'store/store.html', context)


class Cart(APIView):
    def get(self, request):
        context = utils.get_items_orders_and_cart_items(request)
        return render(request, 'store/cart.html', context)


class Checkout(APIView):
    def get(self, request):
        context = utils.get_items_orders_and_cart_items(request)
        return render(request, 'store/checkout.html', context)


class UpdateCartItems(APIView):
    def post(self, request):
        utils.update_cart_items(request)
        return Response({'message': 'Item was added'}, status=status.HTTP_200_OK)


class ProcessOrder(APIView):
    def post(self, request):
        response = utils.process_order_info(request)
        return Response({'message': response['message'], 'transcation_id': response['transaction_id']}, status=status.HTTP_200_OK)


class Login(APIView):
    def get(self, request):
        # check if the user is already logged
        if request.user.is_authenticated:
            return redirect('/store/store.html')

        return render(request, 'store/login.html', {})

    def post(self, request):
        if request.data:
            username = request.data.get('username', '')
            if not username:
                messages.error(request, "Username not found")
                return render(request, 'store/login.html', {})
            password = request.data.get('password', '')
            if not password:
                messages.error(request,'Password not found')
                return render(request, 'store/login.html', {})

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/store/store.html")


class  Register(APIView):
    def get(self, request):
        return ""