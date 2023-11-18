"""
URL configuration for eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('app.urls')),
    path('', views.index, name='index'),
    path('users/login/', views.login_user, name='login'),
    path('users/logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_remove/<int:id>/', views.item_remove, name='item_remove'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart/',views.cart_detail,name='cart'),
    
    #contact
    path('contact/', views.contact, name='contact'),

    #checkout
    path('checkout/', views.checkout, name='checkout'),

    #your Order
    path('order/', views.your_order, name='order'),

    #Product detail page
    path('product/<str:id>/', views.prod_detail, name = 'prod_detail'),

    #Search
    path('search/', views.prod_search, name='search'),



] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
