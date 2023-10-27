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

