from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.

#Rota timeout (Desconectado por inatividade)
def timeout_view(request):
    return render(request, 'timeout.html')

#Login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')