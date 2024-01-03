from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import login,logout,authenticate
from cart.models import Cart,CartItem


def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    return render(request, 'register.html', {'form':form})

def user_profile(request):
    return render(request,'dashboard.html')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)
        
        if user is not None:
            login(request, user)

            # Get or create a cart for the session
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(cart_id=session_key)

            # Assign the user to cart items if cart items exist
            if CartItem.objects.filter(cart=cart).exists():
                cart_items = CartItem.objects.filter(cart=cart)
                for item in cart_items:
                    item.user = user
                    item.save()

            return redirect('profile')  # Redirect to profile page after login

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
