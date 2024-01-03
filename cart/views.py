from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem


def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def cart(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    session_id = get_create_session(request)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user = request.user)
        for item in cart_items:
            total += item.product.price * item.quantity
    else:
        
        cartid = Cart.objects.get(cart_id = session_id) 
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        print(cart_id)
        if cart_id:
            cart_items = CartItem.objects.filter(cart = cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
    print(cart_items)  
    tax = (5*total)/100
    grand_total = total + tax
        
    return render(request, 'cart.html' ,{'cart_items' : cart_items, 'tax' : tax,'total' : total, 'grand_total' : grand_total})




def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_id = get_create_session(request)
    print(session_id)

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=session_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            user=request.user,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    else:
        try:
            cart = Cart.objects.get(cart_id=session_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')




def remove_cart_item(request,product_id):
    product = Product.objects.get(id=product_id)
    session_id=request.session.session_key
    cart_id = Cart.objects.get(cart_id = session_id)
    cart_item = CartItem.objects.get(product=product,cart=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    session_id=request.session.session_key
    cart_id = Cart.objects.get(cart_id = session_id)
    cart_item = CartItem.objects.get(product=product,cart=cart_id)
    cart_item.delete()
    return redirect('cart')


def checkout(request):
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    session_id = get_create_session(request)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user = request.user)
        for item in cart_items:
            total += item.product.price * item.quantity
    else:
        
        cartid = Cart.objects.get(cart_id = session_id) 
        cart_id = Cart.objects.filter(cart_id = session_id).exists()
        print(cart_id)
        if cart_id:
            cart_items = CartItem.objects.filter(cart = cartid)
            for item in cart_items:
                total += item.product.price * item.quantity
    print(cart_items)  
    tax = (5*total)/100
    grand_total = total + tax
    return render(request,'checkout.html',{'cart_items' : cart_items, 'tax' : tax,'total' : total, 'grand_total' : grand_total})
