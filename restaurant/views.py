from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel

class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        #get current date
        today = datetime.today()

        current_user = request.user

        #Get all orders from today
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        
        #loop through the orders and the price value
        #check if order is not shipped
        unshipped_orders = []
        shipped_orders = []

        total_revenue = 0

        for order in orders:
            total_revenue += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)
            elif order.is_shipped:
                shipped_orders.append(order)

        #pass total number of orders and total revenue into template
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


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        current_user = request.user
        
        context = {
            'current_user': current_user,
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/logout/')
