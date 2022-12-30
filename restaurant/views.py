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

        #Извличаме от базата всички поръчки, които са направени днес.
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        
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
        
        context = {
            'current_user': current_user,
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    #Ъпдейтваме базата данни, че поръчката е изпратена, след натискане на бутона "Поръчката е изпратена."
    def post(self, request, pk, *args, **kwargs):
        current_user = request.user
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'current_user': current_user,
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class RestaurantMenu(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        menu_items = Menu.objects.get(restaurant__owner=current_user.id).menu_items

        context = {
            'current_user': current_user, #Подаваме го заради навигацията.
            'menu_items': menu_items
        }

        return render(request, 'restaurant/menu.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/logout/')
