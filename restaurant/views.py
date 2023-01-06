from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel, MenuItem
from restaurant.models import Restaurant, Menu
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import EditForm
from django.views.generic import CreateView, UpdateView, DeleteView


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


#Меню на текущия ресторант.
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


#Меню със статистиките на текущия ресторант.
class Statistics(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        current_user = request.user
        restaurant_name = Restaurant.objects.get(owner=current_user).name
        restaurant_pk = Restaurant.objects.get(owner=current_user).pk

        jan_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 1).filter(restaurant_id=restaurant_pk).count()
        jan_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 1).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        feb_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 2).filter(restaurant_id=restaurant_pk).count()
        feb_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 2).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        march_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 3).filter(restaurant_id=restaurant_pk).count()
        march_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 3).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        april_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 4).filter(restaurant_id=restaurant_pk).count()
        april_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 4).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        may_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 5).filter(restaurant_id=restaurant_pk).count()
        may_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 5).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        june_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 6).filter(restaurant_id=restaurant_pk).count()
        june_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 6).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        july_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 7).filter(restaurant_id=restaurant_pk).count()
        july_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 7).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        aug_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 8).filter(restaurant_id=restaurant_pk).count()
        aug_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 8).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        sep_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 9).filter(restaurant_id=restaurant_pk).count()
        sep_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 9).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        oct_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 10).filter(restaurant_id=restaurant_pk).count()
        oct_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 10).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        nov_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 11).filter(restaurant_id=restaurant_pk).count()
        nov_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 11).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))
        dec_orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 12).filter(restaurant_id=restaurant_pk).count()
        dec_outcome = OrderModel.objects.filter(created_on__year=today.year, created_on__month= 12).filter(restaurant_id=restaurant_pk).aggregate(sum = Sum('price'))

        orders_count_list = [jan_orders, feb_orders, march_orders, april_orders, may_orders, june_orders, july_orders, aug_orders, sep_orders, oct_orders, nov_orders, dec_orders]
        restaurant_outcome_list = [jan_outcome['sum'], feb_outcome['sum'], march_outcome['sum'], april_outcome['sum'], 
                                   may_outcome['sum'], june_outcome['sum'], july_outcome['sum'], aug_outcome['sum'], 
                                   sep_outcome['sum'], oct_outcome['sum'], nov_outcome['sum'], dec_outcome['sum']]

        context = {
            'current_user': current_user,
            'restaurant': restaurant_name,
            'orders_count_list': orders_count_list,
            'restaurant_outcome_list': restaurant_outcome_list
        }

        return render(request, 'restaurant/statistics.html', context)
    
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class EditPage(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        restaurant_name = Restaurant.objects.get(owner=current_user).name

        menu_items = Menu.objects.get(restaurant__owner=current_user.id).menu_items

        context = {
            'current_user': current_user, #Подаваме го заради навигацията.
            'restaurant': restaurant_name,
            'menu_items': menu_items
        }

        return render(request, 'restaurant/edit_page.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class AddItemView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MenuItem
    template_name = 'restaurant/add_item.html'
    fields = '__all__'

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()

class EditItemView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MenuItem
    form_class = EditForm
    template_name = 'restaurant/update_item.html'
    #fields = ['name', 'description', 'price']
    
    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class DeleteItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MenuItem
    template_name = 'restaurant/delete_item.html'
    success_url = reverse_lazy('edit-page')

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()