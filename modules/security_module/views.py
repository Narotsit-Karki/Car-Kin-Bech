from django.shortcuts import render ,  redirect
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate
# Create your views here.

class RegistrationFormView(View):
    form_class = RegistrationForm
    template_name = 'register.html'

    def get(self,request,*args,**kwargs):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # commit false i.e form.save() will not commit to database , committed only after user password is set
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            new_user = form.save(commit=False)
            new_user.set_password(password)

            # commited to database after saving
            new_user.save()
            # authenticate new user
            authenticate()
            auth_user = authenticate(request,username=username,password=password)
            if auth_user is not None:
                messages.success(request,message="Registered and logged in successfully")
                return redirect(reverse('login'))
        
        messages.error(request,message="Registration failed")
        return render(request,self.template_name,{'form':form})
    


            
