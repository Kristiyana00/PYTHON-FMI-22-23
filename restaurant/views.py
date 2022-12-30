from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel, MenuItem
from restaurant.models import Restaurant, Menu
from django.contrib.auth.models import User


#Меню с информация - общо поръчки за деня, обща печалба за деня, текущи поръчки, изпратени поръчки.
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        #Взимаме днешната дата.
        today = datetime.today()

        current_user = request.user

        restaurant_name = Restaurant.objects.get(owner=current_user).name
        restaurant_pk = Restaurant.objects.get(owner=current_user).pk

        #Извличаме от базата всички поръчки, които са направени днес.
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day).filter(restaurant_id=restaurant_pk)
        
        unshipped_orders = []
        shipped_orders = []

        total_revenue = 0

        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)
            elif order.is_shipped:
                shipped_orders.append(order)

        context = {
            'current_user': current_user,
            'restaurant': restaurant_name,
            'shipped_orders': shipped_orders,
            'unshipped_orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


#Меню с детайли за всяка поръчка.
class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        current_user = request.user

        restaurant_name = Restaurant.objects.get(owner=current_user).name
        
        context = {
            'current_user': current_user,
            'restaurant': restaurant_name,
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    #Ъпдейтваме базата данни, че поръчката е изпратена, след натискане на бутона "Поръчката е изпратена."
    def post(self, request, pk, *args, **kwargs):
        current_user = request.user
        restaurant_name = Restaurant.objects.get(owner=current_user).name

        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'current_user': current_user,
            'restaurant': restaurant_name,
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class RestaurantMenu(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        restaurant_name = Restaurant.objects.get(owner=current_user).name

        menu_items = Menu.objects.get(restaurant__owner=current_user.id).menu_items

        context = {
            'current_user': current_user, #Подаваме го заради навигацията.
            'restaurant': restaurant_name,
            'menu_items': menu_items
        }

        return render(request, 'restaurant/menu.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/logout/')
