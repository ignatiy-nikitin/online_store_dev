"""online_store_dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

import products
from products.views import MainView, ProductsByCategoryView

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', MainView.as_view()),
#     path('products/categories/<int:id>/', ProductsByCategoryView.as_view()),
#     path('first/', FirstView.as_view()),
#
#     path('products/<int:id>/', ProductView.as_view()),
#
#     path('import/', ImportView.as_view())
# ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'))),
    path('parsers/', include(('parsers.urls', 'parsers'))),
    path('mail/', include(('send_email.urls', 'send_email'))),
    path('', include(('products.urls', 'products'))),
    # path()
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns_api_v1 = [
#     path('orders/', include(('orders.urls', 'order'))),
#     path('users/', include(('users.urls', 'user'))),
#     path('boxes/', include(('boxes.urls', 'box'))),
#     path('shipments/', include(('shipments.urls', 'shipment'))),
#     path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
# ]
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/', include(urlpatterns_api_v1)),
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
