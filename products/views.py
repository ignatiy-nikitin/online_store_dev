from django.shortcuts import render, get_object_or_404
from django.views import View

from products.forms import SearchProductsForm, OrderForm
from products.models import Category, Product, Vendor


class MainView(View):
    def get(self, request):
        context = {
            'form': SearchProductsForm,
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
            'vendors': Vendor.objects.all(),
        }
        return render(request, 'products/index.html', context)


class ProductsByCategoryView(View):
    def get(self, request, id):
        products = Product.objects.filter(category_id=id)
        context = {
            'categories': Category.objects.all(),
            'category': Category.objects.get(id=id),
            'products': products,
        }
        return render(request, 'products/products_by_category.html', context)


class ProductView(View):
    def get(self, request, id):
        context = {
            'product': get_object_or_404(Product, id=id),
            'form': OrderForm,
        }
        return render(request, 'products/product.html', context)
