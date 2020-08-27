import json
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product, Order, OrderItem, ShippingAddress, Customer, User


def get_items_orders_and_cart_items(request):
    items, order, cart_items = get_cart_items(request)
    return {'items': items, 'order': order, 'cart_items': cart_items, 'is_authenticated': request.user.is_authenticated}


def get_all_products():
    product_objs = Product.objects.all()
    return product_objs


def get_cart_info_from_cookie(request):
    if request.COOKIES and request.COOKIES.get('cart', ''):
        cart = json.loads(request.COOKIES.get('cart'))
        #print('cart', cart)
    else:
        cart = {}

    items = []
    total_no_cart_items = 0
    cart_total_cost = 0.0
    for product_id in cart:  # if there is a COOKIE cart
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product with id {} not found in guest user cookie cart".format(product_id))
        else:
            total_no_cart_items += cart[product_id].get('quantity', 0)
            total_price_of_product = product.price * cart[product_id].get('quantity', 0)
            cart_total_cost += total_price_of_product
            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.name, 'price': product.price,
                            'image': product.image}, 'quantity': cart[product_id]['quantity'],
                'digital': product.digital, 'get_total_price': total_price_of_product,
            }
            items.append(item)

    return {'items': items, 'total_no_cart_items': total_no_cart_items, 'cart_total_cost': cart_total_cost}


def get_cart_items(request):
    if request.user.is_authenticated:  # if user is logged in
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,
                                                     complete=False)  # get any pending orders to cart
        items = order.orderitem_set.all()  # get items for the order
        cart_items = order.get_no_cart_items  # get total no of cart items
    else:
        # check if cookie 'cart' is present and take values from it
        cart_info = get_cart_info_from_cookie(request)
        items = cart_info['items']
        order = {'get_cart_total': cart_info['cart_total_cost'], 'get_no_cart_items': cart_info['total_no_cart_items']}
        cart_items = order.get('get_no_cart_items')

    return items, order, cart_items


def update_cart_items(request):
    if request.data:
        product_id = request.data.get('productId', '')
        if not product_id:
            raise Exception("Product Id Not Found")
        action = request.data.get('action', '')
        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        # get if any pending orders are there in the user's cart by adding complete=False
        # if no orders pending then this creates one.
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # get orderitems for the order. If the product is not added to the order then this creates a new entry
        # to the order. so that the existing cart updates.
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1

        if order_item.quantity <= 0:
            order_item.delete()
        else:
            order_item.save()


def create_transaction_id():
    transaction_id = str(uuid.uuid4())[:7]
    return transaction_id


def create_shipping_order_info(customer, order, address, city, state, zipcode):
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=address,
        city=city,
        state=state,
        zipcode=zipcode
    )


def create_guest_order(request):
    data = request.data
    name = data.get('form').get('name', '')
    email = data.get('form').get('email', '')
    if not name or not email:
        raise Exception("Guest Name or Email is not entered.")
    cart_info = get_cart_info_from_cookie(request)
    items = cart_info['items']
    # get or create customer for guest user. Even though guest doesn't want to login, for tracking the orders
    # we need to create a customer and assign the orderItems and order to the customer.
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return order, customer


def process_order_info(request):
    if request.data:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)

        else:
            # process guest user order
            order, customer = create_guest_order(request)

        data = request.data
        shipping_info = data.get('shipping', '')

        if not shipping_info:
            raise Exception("Shipping info not found")

        form = data.get('form', '')
        if form:
            total = float(form.get('total', ''))
        if total != 0 and total == order.get_cart_total:
            order.complete = True
            order.transaction_id = create_transaction_id()
            order.save()
            create_shipping_order_info(customer, order, shipping_info.get('address', ''),
                                       shipping_info.get('city', ''),
                                       shipping_info.get('state', ''),
                                       shipping_info.get('zipcode', ''))
            return {'transaction_id': order.transaction_id, 'message': 'order processed and submitted for payment'}
        raise Exception("Order total is zero")

    raise Exception("Process order info not found")


def validate_login(request):
    if request.data:
        username = request.data.get('username', '')
        if not username:
            messages.error(request, "Username not found")
            return False, request

        password = request.data.get('password', '')
        if not password:
            messages.error(request, 'Password not found')
            return False, request

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return True, request
        messages.error(request, "User credentials are wrong")
        return False, request

    raise Exception("Request data not found in registration")


def register_user(email, name, password, request):
    user = User(email=email, first_name=name)
    user.set_password(password)
    user.save()
    customer = Customer(user=user, email=email, name=name)
    customer.save()
    messages.success(request, "User registered! Please login.")
    return True, request


def validate_register_user_details(request):
    if request.data:
        email = request.data.get('email', '')
        name = request.data.get('name', '')
        pass1 = request.data.get('password1', '')
        pass2 = request.data.get('password2', '')
        if not email or not pass1 or not pass2 or not name:
            messages.error(request, "Entered details are blank")
            return False, request
        if pass1 != pass2:
            messages.error(request, "Entered passwords are not matching")
            return False, request

        return register_user(email, name, pass1, request)
    raise Exception("Request data not found in the registration")