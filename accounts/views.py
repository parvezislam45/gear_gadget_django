from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart')
    return render(request, 'register.html', {'form':form})

def user_profile(request):
    return render(request,'dashboard.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = user_name, password = password)
        print(user)
        login(request, user)
        return redirect('profile')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
