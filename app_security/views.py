from django.shortcuts import render
from .forms import LoginForm, RegistrationForm


# Create your views here.
def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        messages.success(request, 'Login successful!')
        return redirect('home')
    return render(request, 'login.html', {'form': form})

def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        messages.success(request, 'Registration successful!')
        return redirect('home')

    return render(request, 'Register.html', {'form': form})