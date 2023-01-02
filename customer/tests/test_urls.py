from django.test import SimpleTestCase
from django.urls import reverse, resolve
from customer.views import *


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func.view_class, Index)

    def test_avout_url_is_resolves(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func.view_class, About)
    
    def test_general_menu_url_is_resolves(self):
        url = reverse('general-menu')
        self.assertEquals(resolve(url).func.view_class, GeneralMenuView)

    def test_general_menu_search_url_is_resolves(self):
        url = reverse('general-menu-search')
        self.assertEquals(resolve(url).func.view_class, GeneralMenuSearchView)
    
    def test_restaurants_url_is_resolves(self):
        url = reverse('restaurants')
        self.assertEquals(resolve(url).func.view_class, Restaurants)

    def test_customer_restaurant_menu_url_is_resolves(self):
        url = reverse('customer-restaurant-menu', args=[1])
        self.assertEquals(resolve(url).func.view_class, CustomerRestaurantMenu)
    
    def test_restaurant_menu_search_url_is_resolves(self):
        url = reverse('restaurant-menu-search', args=[1])
        self.assertEquals(resolve(url).func.view_class, RestaurantMenuSearch)
    
    def test_restaurants_search_url_is_resolves(self):
        url = reverse('restaurants-search')
        self.assertEquals(resolve(url).func.view_class, RestaurantSearch)
    
    def test_choose_restauranta_to_order_url_is_resolves(self):
        url = reverse('choose-restaurant-order')
        self.assertEquals(resolve(url).func.view_class, ChooseRestaurantOrder)
    
    def test_order_menu_url_is_resolves(self):
        url = reverse('order-menu', args=[1])
        self.assertEquals(resolve(url).func.view_class, OrderMenu)
    
    def test_order_confirmation_url_is_resolves(self):
        url = reverse('order-confirmation', args=[1])
        self.assertEquals(resolve(url).func.view_class, OrderConfirmation)
    
    def test_order_payment_confirmation_url_is_resolves(self):
        url = reverse('payment-confirmation')
        self.assertEquals(resolve(url).func.view_class, OrderPayConfirmation)