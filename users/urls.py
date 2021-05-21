from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import LogInView, OrderInfoView, RegisterView, LogOutView, AccountView, BasketView, CreateFinalOrderView, OrdersView, SendViewSet

api_router = DefaultRouter()
api_router.register('send', SendViewSet, basename='send')


urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('basket/create_final_order/', CreateFinalOrderView.as_view(), name='create_final_order'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:id>/', OrderInfoView.as_view(), name='order-info'),
    # path('orders/send/<int:id>/', )
]

urlpatterns += api_router.urls