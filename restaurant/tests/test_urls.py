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

    def test_restaurant_edit_page_url_resolves(self):
        url = reverse('edit-page')
        self.assertEquals(resolve(url).func.view_class, EditPage)

    def test_restaurant_edit_item_url_resolves(self):
        url = reverse('edit-info', args=[1])
        self.assertEquals(resolve(url).func.view_class, EditItemView)
    
    def test_restaurant_delete_item_url_resolves(self):
        url = reverse('delete-item', args=[1])
        self.assertEquals(resolve(url).func.view_class, DeleteItemView)

    def test_restaurant_add_item_page_url_resolves(self):
        url = reverse('add-item')
        self.assertEquals(resolve(url).func.view_class, AddItemView)