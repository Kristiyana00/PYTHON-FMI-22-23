import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, OrderModel, Category

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html' )


class Order(View):
    def get(self, request, *args, **kwargs):
        #get every item from each category
        salads = MenuItem.objects.filter(category__name__contains='Салата')
        appetizers = MenuItem.objects.filter(category__name__contains='Предястие')
        main_dishes = MenuItem.objects.filter(category__name__contains='Основно ястие')
        drinks = MenuItem.objects.filter(category__name__contains='Напитки')
        deserts = MenuItem.objects.filter(category__name__contains='Десерт')
        seafood = MenuItem.objects.filter(category__name__contains='Морски дарове')
        italian = MenuItem.objects.filter(category__name__contains='Паста и ризото')
        pizzas = MenuItem.objects.filter(category__name__contains='Пици')
        sushi = MenuItem.objects.filter(category__name__contains='Суши')
        
        #pass into context
        context = {
            'salads': salads,
            'appetizers': appetizers,
            'main_dishes': main_dishes,
            'drinks': drinks,
            'deserts': deserts,
            'seafood': seafood,
            'italian': italian,
            'pizzas': pizzas,
            'sushi': sushi,
        }

        #render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]') #list s pk

        for item in items:
            #взимаме item-a от базата данни с id което е в листа
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            #dobavqme v spisuka s items
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
             price += item['price']
             item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            country=country,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        body = ('Благодарим за направената поръчка! Храната ти се приготвя и ще бъде доставена възможно най-скоро!\n'
            f'Обща сума: {price}\n'
            'Благодарим отново за доверието!')

        #Send confirmation email
        send_mail(
            'Благодарим за направената поръчка!',
            body,
            'foody@gmail.com',
            [email],
            fail_silently=False
        )

        context = {
             'items': order_items['items'],
             'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            #Search by name
            Q(name__icontains=query) | 
            #Search by price
            Q(price__icontains=query) |
            #Search by description of menu item
            Q(description__icontains=query) |
            #Search by category
            Q(category__name__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)