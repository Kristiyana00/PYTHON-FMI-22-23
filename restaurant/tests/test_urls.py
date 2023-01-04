from django.test import SimpleTestCase
from django.urls import reverse, resolve
from restaurant.views import *

class TestUrls(SimpleTestCase):
    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func.view_class, Dashboard)
    
    def test_order_details_url_resolves(self):
        url = reverse('order-details', args=[1])
        self.assertEquals(resolve(url).func.view_class, OrderDetails)
    
    def test_restaurant_menu_url_resolves(self):
        url = reverse('restaurant-menu')
        self.assertEquals(resolve(url).func.view_class, RestaurantMenu)
    
    def test_restaurant_statisticks_url_resolves(self):
        url = reverse('statistics')
        self.assertEquals(resolve(url).func.view_class, Statistics)