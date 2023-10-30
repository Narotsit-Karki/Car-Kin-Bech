from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control my-3 small-textbox border-primary'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control my-3 small-textbox border-primary'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn login-button w-100'))

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=20)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    user_type = forms.ChoiceField(choices=[(1, 'Buyer'), (2, 'Seller')], label='What Are You?')
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login', css_class='btn login-button w-100'))