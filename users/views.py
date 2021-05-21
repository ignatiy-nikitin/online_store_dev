from users.serializers import OrderFinalSerializer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from orders.forms import CreateFinalOrderForm
from orders.models import Order, OrderFinal, OrderItem
from parsers.email import send_email

from users.forms import EditAccountForm, LogInForm, RegisterForm
from users.models import User

from rest_framework import viewsets


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:main')  # TODO: not correct
        return render(request, 'users/login2.html', {'form': LogInForm})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('products:main')
        context = {
            'form': LogInForm,
        }
        messages.add_message(request, messages.ERROR,
                             'Неверный логин или пароль')
        return render(request, 'users/login2.html', context)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:main')
        context = {
            'form': RegisterForm,
        }
        return render(request, 'users/register2.html', context)

    def post(self, request):
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Пользователь с таким логином уже существует')
            return redirect('users:register')
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        login(request, user)
        return redirect('products:main')


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('products:main')


class AccountView(View):
    def get(self, request):
        return render(request, 'users/account-edit.html', {'form': EditAccountForm})


class BasketView(View):
    def get(self, request):

        print('-----', self.request.user.order.order_items)
        context = {
            'order': self.request.user.order,
            'order_items': self.request.user.order.order_items.filter(quantity__gt=0),
            'form': CreateFinalOrderForm,
            # 'order_items': OrderItem.objects.all()
        }
        return render(request, 'users/basket2.html', context)

    def post(self, request):
        form = CreateFinalOrderForm(request.POST)
        print('HERE')
        if form.is_valid():
            print('HERE 2')
            form = form.save(commit=False)
            # order = Order.objects.get(user=self.request.user)
            form.recipient = self.request.user
            form.order = self.request.user.order
            form.total_cost = self.request.user.order.total_cost
            form.save()

            send_email(form, self.request.user)

            # order.delete()
            # return redirect('products:main')
            # (f'/users/orders/{id}/')
            return redirect('users:order-info', id=form.id)


class OrdersView(View):
    def get(self, request):
        context = {
            'orders_final': self.request.user.orders_final.all(),
        }
        return render(request, 'users/orders.html', context)


class OrderInfoView(View):
    def get(self, request, id):
        context = {
            'order': OrderFinal.objects.get(id=id),
        }
        return render(request, 'users/order_info2.html', context)


class CreateFinalOrderView(View):
    def get(self, request):
        context = {
            'form': CreateFinalOrderForm,
        }
        return render(request, 'users/create_final_order.html', context)

    def post(self, request):
        form = CreateFinalOrderForm(request.POST)
        print('HERE')
        if form.is_valid():
            print('HERE 2')
            form = form.save(commit=False)
            # order = Order.objects.get(user=self.request.user)
            form.recipient = self.request.user
            form.order = self.request.user.order
            form.total_cost = self.request.user.order.total_cost
            form.save()

            send_email(form, self.request.user)

            # order.delete()
            return redirect('users:order-info', id=id)

            # created_dt = models.DateTimeField(auto_now_add=True)
            # delivery_dt = models.DateTimeField()
            # recipient = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='orders_final')
            # address = models.CharField(max_length=256)
            # cart = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='orders_final')
            # status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='orders_final')
            # total_cost = models.DecimalField(max_digits=8, decimal_places=2)

        # def post(self, request, id):
        #     order_instance = OrderItem.objects.filter(order__user=self.request.user, product__id=id).first()
        #     order_instance = order_instance if order_instance else None
        #     form = OrderForm(request.POST, instance=order_instance)
        #     if form.is_valid():
        #         form = form.save(commit=False)
        #         if Order.objects.filter(user=self.request.user).exists():
        #             order = Order.objects.get(user=self.request.user)
        #         else:
        #             order = Order.objects.create(user=self.request.user)
        #         form.order = order
        #         product = Product.objects.get(id=id)
        #         form.product = product
        #         form.price = product.price
        #         form.save()
        #         return redirect('products:products:product', id=id)



#  API

class SendViewSet(viewsets.ModelViewSet):
    serializer_class = OrderFinalSerializer

    def get_object(self):
        order = get_object_or_404(OrderFinal, id=self.kwargs['pk'])
        order.delivery_time_from = str(order.delivery_time_from)[:2] + str(order.delivery_time_from)[3:5] + '00'
        order.delivery_time_to = str(order.delivery_time_to)[:2] + str(order.delivery_time_to)[3:5] + '00'
        return order