from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from orders.models import OrderItem

from products.forms import OrderForm, SearchProductsForm
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
        order_instance = None
        context = {
            'product': get_object_or_404(Product, id=id),
            'some_extra_data': 'some_extra_data',
        }
        if request.user.is_authenticated:
            order_instance = self.request.user.order.order_items.filter(
                order__user=self.request.user, product__id=id).first()
            context['total_price'] = order_instance.total_price if order_instance else 0
            order_instance = order_instance if order_instance else None
            context['form'] = OrderForm(instance=order_instance)
        return render(request, 'products/product.html', context)

    def post(self, request, id):
        order_instance = OrderItem.objects.filter(
            order__user=self.request.user, product__id=id).first()
        order_instance = order_instance if order_instance else None
        form = OrderForm(request.POST, instance=order_instance)
        if form.is_valid():
            form = form.save(commit=False)
            # if Order.objects.filter(user=self.request.user).exists():
            #     order = Order.objects.get(user=self.request.user)
            # else:
            #     order = Order.objects.create(user=self.request.user)
            form.order = self.request.user.order
            product = Product.objects.get(id=id)
            form.product = product
            form.price = product.price
            form.save()
            return redirect('products:products:product', id=id)
