from django.urls import path

from users.views import LogInView, RegisterView, LogOutView, AccountView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='logout'),
]
