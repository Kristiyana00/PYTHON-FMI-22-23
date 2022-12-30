import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, OrderModel, Category
from restaurant.models import Restaurant, Menu

#Заглавна страница на сайта.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    

#Секция За Нас:
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html' )


#Меню за избор от кой ресторант да поръчаш храна.
class ChooseRestaurantOrder(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()

        context = {
            'restaurants': restaurants
        }

        return render(request, 'customer/order.html', context)


#Меню за самата поръчка - извлича цялата информация - избрани продукти и данни на потребителя.
class OrderMenu(View):
    def get(self, request, pk, *args, **kwargs):
        #get every item from each category
        # salads = MenuItem.objects.filter(category__name__contains='Салата')
        # appetizers = MenuItem.objects.filter(category__name__contains='Предястие')
        # main_dishes = MenuItem.objects.filter(category__name__contains='Основно ястие')
        # drinks = MenuItem.objects.filter(category__name__contains='Напитки')
        # deserts = MenuItem.objects.filter(category__name__contains='Десерт')
        # seafood = MenuItem.objects.filter(category__name__contains='Морски дарове')
        # italian = MenuItem.objects.filter(category__name__contains='Паста и ризото')
        # pizzas = MenuItem.objects.filter(category__name__contains='Пици')
        # sushi = MenuItem.objects.filter(category__name__contains='Суши')

        restaurant = Restaurant.objects.get(pk=pk)
        salads = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Салата')
        appetizers = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Предястие')
        main_dishes = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Основно ястие')
        drinks = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Напитки')
        deserts = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Десерт')
        seafood = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Морски дарове')
        italian = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Паста и ризото')
        pizzas = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Пици')
        sushi = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(category__name__contains='Суши')
        
        #pass into context
        context = {
            'pk': pk,
            'restaurant': restaurant,
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
        return render(request, 'customer/order_menu.html', context)

    def post(self, request, pk, *args, **kwargs):
        restaurant_id = Restaurant.objects.get(pk=pk).pk
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
            #Взимаме item-a от базата данни с id, което е в листа.
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            #Добавяме в списъка с поръчани неща.
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
             price += item['price']
             item_ids.append(item['id'])

        #Създаваме поръчка и я инициализираме с вече събраните данни.
        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            country=country,
            zip_code=zip_code,
            restaurant_id=restaurant_id
        )
        #Добавяме всички неща от кошницата към поръчката.
        order.items.add(*item_ids)

        #Инициализираме body-то на имейла.
        body = ('Благодарим за направената поръчка! Храната Ви се приготвя и ще бъде доставена възможно най-скоро!\n'
            f'Обща сума: {price}\n'
            'Благодарим отново за доверието!')

        #Изпращане на потвърждаващ имейл на потребителя.
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
        

#Меню за потвърждаване на поръчката.
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    #Ако потребителят плати чрез PayPal, ъпдейтваме базата данни, че поръчката е вече платена.
    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


#Потвърждение на плащането.
class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


#Меню с всички ресторанти на сайта.
class Restaurants(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()

        context = {
            'restaurants': restaurants
        }

        return render(request, 'customer/restaurants.html', context)


#Търсачка в менюто с ресторанти - търсене на ресторант по име.
class RestaurantSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        restaurants = Restaurant.objects.filter(
            #Search by name
            Q(name__icontains=query)
        )

        context = {
            'restaurants': restaurants
        }

        return render(request, 'customer/restaurants.html', context)


#Менюто на избрания от потребителя ресторант.
class CustomerRestaurantMenu(View):
    def get(self, request, pk, *args, **kwargs):
        restaurant = Restaurant.objects.get(pk=pk)
        menu_items = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items

        context = {
            'pk': pk,
            'restaurant': restaurant,
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


#Търсачка в менюто на избрания от потребителя ресторант - търсене по име, цена, описание на продукта и категория.
class RestaurantMenuSearch(View):
    def get(self, request, pk, *args, **kwargs):
        query = self.request.GET.get("q")

        restaurant = Restaurant.objects.get(pk=pk)

        menu_items = Menu.objects.get(restaurant__name__contains=restaurant.name).menu_items.filter(
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
            'pk': pk,
            'restaurant': restaurant,
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


#Меню с всички налични продукти, които се предлагат в сайта.
class GeneralMenuView(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/general_menu.html', context)


#Търсачка в менюто с всички налични продукти - търсене по име, цена, описание на продукта и категория.
class GeneralMenuSearchView(View):
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

        return render(request, 'customer/general_menu.html', context)