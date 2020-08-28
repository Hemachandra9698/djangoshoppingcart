from django.contrib.auth import logout
from django.shortcuts import render, redirect
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
            return redirect('store')  # redirect to store.html -> homepage
        context = utils.get_items_orders_and_cart_items(request)
        return render(request, 'store/login.html', context)

    def post(self, request):
        login, request = utils.validate_login(request)
        context = utils.get_items_orders_and_cart_items(request)
        if not login:
            return render(request, 'store/login.html', context)
        return redirect('store')  # redirect to homepage


class Register(APIView):
    def get(self, request):
        context = utils.get_items_orders_and_cart_items(request)
        return render(request, 'store/register.html', context)

    def post(self, request):
        register, request =  utils.validate_register_user_details(request)
        context = utils.get_items_orders_and_cart_items(request)
        if not register:
            return render(request, 'store/register.html', context)
        return render(request, 'store/login.html', context)


class Logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('store') # redirect to home page


class ProductView(APIView):
    def get(self, request, product_id):
        context = utils.get_items_orders_and_cart_items(request)
        context['product'] = utils.get_product_context(product_id)
        return render(request, "store/productpage.html", context)
