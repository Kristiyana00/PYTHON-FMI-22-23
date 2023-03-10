from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
from django.urls import reverse
from restaurant.views import *


class TestViews(TestCase):
    def setUp(self):
        group_name = 'Staff'
        self.group = Group(name=group_name)
        self.group.save()
        self.client = Client()

        self.user = User.objects.create_user(
            username='restaurant_test', 
            email='restaurant_test@example.com', 
            password='test')

        self.restaurant = Restaurant.objects.create(
            owner=self.user, 
            name='Test Restaurant')

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

        self.menu = Menu.objects.create(
            menu_name='Test Menu',
            #menu_items=[]
            restaurant=self.restaurant
        )

        self.menu_item = MenuItem.objects.create(
            name='Test',
            description='Test',
            price=9.99
        )
    
    def tearDown(self):
        self.user.delete()
        self.group.delete()
        self.restaurant.delete()
        self.order.delete()
        self.menu.delete()
        self.menu_item.delete()

    #Test Dashboard View:
    def test_user_cannot_access_dashboard(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')

    def test_user_can_access_dashboard(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/dashboard.html')

    #Test OrderDetails View:
    def test_user_cannot_access_order_details_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('order-details', args=[1]))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')

    def test_user_can_access_order_details_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('order-details', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/order-details.html')
    
    #TODO:
    # def test_order_details_POST(self):
    #     pass

    #Test RestaurantMenu View:
    def test_user_cannot_access_restaurant_menu_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('restaurant-menu'))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')

    def test_user_can_access_restaurant_menu_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('restaurant-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/menu.html')

    #Test Statistics View:
    def test_user_cannot_access_restaurant_statistics_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')
    
    def test_user_can_access_restaurant_statistics_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/statistics.html')

    #Test EditPage View:
    def test_user_cannot_access_restaurant_edit_page_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('edit-page'))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')
    
    def test_user_can_access_restaurant_edit_page_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('edit-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/edit_page.html')

    #Test AddItem View:
    def test_user_cannot_access_restaurant_add_item_page_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('add-item'))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')
    
    def test_user_can_access_restaurant_add_item_page_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('add-item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/add_item.html')

    #Test EditItem View:
    def test_user_cannot_access_restaurant_edit_item_page_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('edit-info', args=[1]))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')
    
    def test_user_can_access_restaurant_edit_item_page_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('edit-info', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/update_item.html')

    #Test DeleteItem View:
    def test_user_cannot_access_restaurant_delete_item_page_GET(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('delete-item', args=[1]))
        self.assertEqual(response.status_code, 403, u'Forbidden page. Only group members can access the page.')
    
    def test_user_can_access_restaurant_delete_item_page_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('delete-item', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_item.html')

    #Test Logout View:
    def test_logout(self):
        self.client.login(username='restaurant_test', password='test')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)