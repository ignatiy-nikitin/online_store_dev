from django.urls import path, include

from products.views import MainView, ProductsByCategoryView, ProductView

urlpatterns_products = [
    path('categories/<int:id>/', ProductsByCategoryView.as_view()),
    # path('first/', FirstView.as_view()),
    #
    path('<int:id>/', ProductView.as_view()),
    #
    # path('import/', ImportView.as_view())
]


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('products/', include(urlpatterns_products))
]
