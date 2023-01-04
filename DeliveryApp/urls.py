"""DeliveryApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from customer.views import Index, About, OrderMenu, OrderConfirmation,\
                           OrderPayConfirmation, GeneralMenuView, GeneralMenuSearchView,\
                           Restaurants, RestaurantSearch, CustomerRestaurantMenu,\
                           RestaurantMenuSearch, ChooseRestaurantOrder
from restaurant.views import Logout, Dashboard, OrderDetails, RestaurantMenu, Statistics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('general_menu/', GeneralMenuView.as_view(), name='general-menu'),
    path('general_menu/search/', GeneralMenuSearchView.as_view(), name='general-menu-search'),
    path('restaurants/', Restaurants.as_view(), name='restaurants'),
    path('restaurants/<int:pk>/menu/', CustomerRestaurantMenu.as_view(), name='customer-restaurant-menu'),
    path('restaurants/<int:pk>/menu/search/', RestaurantMenuSearch.as_view(), name='restaurant-menu-search'),
    path('restaurants/search/', RestaurantSearch.as_view(), name='restaurants-search'),
    path('restaurants/order/', ChooseRestaurantOrder.as_view(), name='choose-restaurant-order'),
    path('restaurants/order/<int:pk>/order_menu/', OrderMenu.as_view(), name='order-menu'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('accounts/logout/', Logout.as_view(), name='logout'),
    path('restaurant/dashboard/', Dashboard.as_view(), name='dashboard'),
    path('restaurant/orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('restaurant/menu/', RestaurantMenu.as_view(), name='restaurant-menu'),
    path('restaurant/statistics/', Statistics.as_view(), name='statistics')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
