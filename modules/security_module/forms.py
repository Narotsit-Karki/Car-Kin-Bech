from django import forms
from django.contrib.auth.forms import AuthenticationForm , UsernameField
from common.models import KinBechUser
from crispy_forms.helper import FormHelper
FIELD_CLASS_NAME = "form-control mt-3 border-primary"

class LoginForm(AuthenticationForm):

   
    username = UsernameField(widget=forms.TextInput(attrs={'class':FIELD_CLASS_NAME}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':FIELD_CLASS_NAME}))

    
    # overriding default Authentication Form constructor
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        # set same class to all fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = FIELD_CLASS_NAME
    
    class Meta:
        model = KinBechUser
        fields = [
            'first_name','last_name','email','phone','username','password','password2' ,'user_type'
            ]
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if '@gmail' not in email:
            raise forms.ValidationError('only gmail is accepted')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(str(phone)) > 10:
            raise forms.ValidationError('provide valid phone number')
        return phone
    
    def clean_password2(self):
        password  = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('password donot match')
        else:
            return password2
        
