from django.test import TestCase, Client
from django.urls import reverse
from customer.views import *
from restaurant.models import *
from customer.models import *
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='restaurant_test', 
            email='restaurant_test@example.com', 
            password='test')

        self.restaurant = Restaurant.objects.create(
            owner=self.user, 
            name='Test Restaurant',
            logo='test-logo.jpg')

        self.menu = Menu.objects.create(
            menu_name='Test Menu',
            #menu_items=[]
            restaurant=self.restaurant
        )

        self.category = Category.objects.create(name='Test')

        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test',
            price=9.99,
            image='test-logo.jpg'
        )
        self.menu_item.category.add(self.category)
        self.menu_item.save()

        self.order = OrderModel.objects.create(
            price=99.99,
            #items=[]
            name='Test',
            email='test@test.com',
            street='Test Str.',
            city='Test',
            country='Test',
            zip_code=1000,
            restaurant_id=self.restaurant.pk
        )

        self.menu.menu_items.add(self.menu_item)
        self.menu.save()
    
    def tearDown(self):
        self.user.delete()
        self.restaurant.delete()
        self.menu.delete()
        self.order.delete()
    
    #Test Index View:
    def test_index_GET(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/index.html')
    
    #Test About View:
    def test_about_GET(self):
        response = self.client.get(reverse('about'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/about.html')

    #Test ChooseRestaurantOrder View:
    def test_choose_restaurant_order_GET(self):
        response = self.client.get(reverse('choose-restaurant-order'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/order.html')
    
    #Test OrderMenu View:
    def test_order_menu_GET(self):
        response = self.client.get(reverse('order-menu', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/order_menu.html')

    def test_order_menu_POST(self):
        url = reverse('order-menu', args=[1])
        response = self.client.post(url, {
            'items[]': 1,
            'name': 'Test Name',
            'email': 'test@example.com',
            'street': 'Street Test',
            'city': 'Sofia',
            'country': 'Bulgaria',
            'zip': 1000
        })

        order = OrderModel.objects.get(id=2)
        self.assertEquals(order.name, 'Test Name')
        self.assertEquals(order.email, 'test@example.com')
        self.assertEquals(order.street, 'Street Test')
        self.assertEquals(order.city, 'Sofia')
        self.assertEquals(order.country, 'Bulgaria')
        self.assertEquals(order.zip_code, 1000)

        self.assertEquals(response.status_code, 302, u'Redirected to Order Confirmation.')
        self.assertRedirects(response, '/order-confirmation/2', status_code=302, target_status_code=200, fetch_redirect_response=True)

    #Test OrderConfirmation View:
    def test_order_confirmation_GET(self):
        response = self.client.get(reverse('order-confirmation', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/order_confirmation.html')
    
    #TODO:
    # def test_order_confirmation_POST(self):
    #     pass

    #Test OrderPayConfirmation View:
    def test_order_payment_confirmation_GET(self):
        response = self.client.get(reverse('payment-confirmation'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/order_pay_confirmation.html')

    #Test Restaurants View:
    def test_restaurants_GET(self):
        response = self.client.get(reverse('restaurants'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/restaurants.html')

    #Test RestaurantSearch View:
    def test_restaurant_search_GET(self):
        url = '{url}?{filter}={value}'.format(
            url = reverse('restaurants-search'),
            filter='q',
            value='Test'
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/restaurants.html')

    #Test CustomerRestaurantMenu View:
    def test_customer_restaurant_menu_GET(self):
        response = self.client.get(reverse('customer-restaurant-menu', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/menu.html')
    
    #Test RestaurantMenuSearch View:
    def test_restaurant_menu_search_GET(self):
        url = '{url}?{filter}={value}'.format(
            url = reverse('restaurant-menu-search', args=[1]),
            filter='q',
            value='Test'
        )
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/menu.html')

    #Test GeneralMenuView View:
    def test_general_menu_GET(self):
        response = self.client.get(reverse('general-menu'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/general_menu.html')

    #Test GeneralMenuSearchView View:
    def test_general_menu_search_GET(self):
        url = '{url}?{filter}={value}'.format(
            url = reverse('general-menu-search'),
            filter='q',
            value='Test'
        )
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/general_menu.html')