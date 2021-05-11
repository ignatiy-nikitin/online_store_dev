from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LogInForm, RegisterForm, EditAccountForm


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:main')  # TODO: not correct
        return render(request, 'users/login.html', {'form': LogInForm})

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
        messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
        return render(request, 'users/login.html', context)


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('products:main')
        context = {
            'form': RegisterForm,
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Пользователь с таким логином уже существует')
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
