from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-food/', views.add_food, name='add_food'),
    path('update-food/<int:id>/', views.update_food, name='update_food'),
    path('delete-food/<int:id>/', views.delete_food, name='delete_food'),
    path('login/', views.user_login, name='login'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('logout/', views.user_logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.my_orders, name='orders'),
    path('update-cart/<int:id>/<str:action>/', views.update_cart, name='update_cart'),
    path('payment/', views.payment, name='payment'),
    path('place-order/', views.place_order, name='place_order'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('offers/', views.offers, name='offers'),
    path('admin-report/', views.admin_report, name='admin_report'),
]