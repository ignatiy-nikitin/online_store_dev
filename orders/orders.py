from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, ButtonHolder
from django import forms
from django.contrib.auth.models import User
#
# from junior.models import Company, Application, Vacancy, Resume



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']
        labels = {
            'written_username': 'Вас зовут',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.label_class = 'mb-1'
        self.helper.add_input(Submit('submit', 'Записаться на пробный урок', css_class='btn btn-primary mt-4 mb-2'))
        self.helper.layout = Layout(
            Row(
                Column('written_username'),
            ),
            Row(
                Column('written_phone'),
            ),
            Row(
                Column('written_cover_letter'),
            ),
        )