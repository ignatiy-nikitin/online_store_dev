from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Column
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'text-muted'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='button button-register w-100', text_color='white'))
        self.fields['username'].help_text = None
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class LogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Логин',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'text-muted'
        self.helper.add_input(Submit('submit', 'Войти', css_class='button button-login w-100'))
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs.update({'class': 'form-control'})


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'mb-2 text-dark'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='btn btn-info'))
        self.helper.layout = Layout(
            Column('username'),
            Column('password'),

            # Row(Column('status'), Column('salary')),
            # Row(Column('specialty'), Column('grade')),
            # Row(Column('education')),
            # Row(Column('experience')),
            # Row(Column('portfolio')),
        )
