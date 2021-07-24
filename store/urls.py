from django.urls import path
from . import views

urlpatterns = [
    path('', views.Store.as_view(), name='store'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('update-item/', views.UpdateCartItems.as_view(), name='update_item'),
    path('process-order/', views.ProcessOrder.as_view(), name='process_order'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('product-page/<int:product_id>/', views.ProductView.as_view(), name='product_page' )
]