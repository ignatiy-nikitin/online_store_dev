from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, ButtonHolder
from crispy_forms import layout
from django import forms

from orders.models import OrderItem
from products.models import Product


class SearchProductsForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Поиск...'}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.label_class = 'mb-2 text-dark'
        self.helper.form_action = '/search/'
        self.helper.layout = Layout(
            Row(Column('query'), Column(ButtonHolder(
                Submit('', 'Найти товары', css_class='btn btn-primary  my-0')
            )))
        )


BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
        labels = {
            'quantity': 'Количество товара'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'mb-2 text-dark'
        self.helper.layout = Layout(
            Row(Column('quantity')),
            Row(Column(ButtonHolder(
                Submit('', 'Добавить в корзину', css_class='btn btn-primary  my-0')
            )))
        )




    # quantity = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), label='Количество товара')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'get'
    #     self.helper.label_class = 'mb-2 text-dark'
    #     self.helper.form_action = '/search/'
    #     self.helper.layout = Layout(
    #         Row(Column('quantity')),
    #         Row(Column('query'), Column(ButtonHolder(
    #             Submit('', 'Найти товары', css_class='btn btn-primary  my-0')
    #         )))
    #     )

#
# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['written_username', 'written_phone', 'written_cover_letter']
#         labels = {
#             'written_username': 'Вас зовут',
#             'written_phone': 'Ваш телефон',
#             'written_cover_letter': 'Сопроводительное письмо',
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#
#         self.helper.form_method = 'post'
#         self.helper.label_class = 'mb-1'
#         self.helper.add_input(Submit('submit', 'Записаться на пробный урок', css_class='btn btn-primary mt-4 mb-2'))
#         self.helper.layout = Layout(
#             Row(
#                 Column('written_username'),
#             ),
#             Row(
#                 Column('written_phone'),
#             ),
#             Row(
#                 Column('written_cover_letter'),
#             ),
#         )