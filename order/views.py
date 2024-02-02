from django.shortcuts import render,redirect
from cart.models import Cart,CartItem
from .forms import OrderForm
from .models import Payment, OrderProduct, Order
from .ssl import sslcommerz_payment_gateway
from store.models import Product
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@csrf_exempt
def success_view(request):
    if request.method == 'POST':
        data = request.POST
        user_id = int(data['value_b']) 
        user = User.objects.get(pk=user_id)
        
        payment = Payment(
            user=user,
            payment_id=data['tran_id'],
            payment_method=data['card_issuer'],
            amount_paid=float(data['store_amount']),  # Convert to float instead of int
            status=data['status'],
            # Assuming created_at is auto-managed (e.g., auto_now_add=True)
            # No need to explicitly set it; it will be automatically managed by Django
        )
        payment.save()
        
        order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        cart_items = CartItem.objects.filter(user=user)
        for item in cart_items:
            order_product = OrderProduct(
                order=order,
                payment=payment,
                user=user,
                product=item.product,
                quantity=item.quantity,
                ordered=True
            )
            order_product.save()

            product = Product.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()

        CartItem.objects.filter(user=user).delete()
        return redirect('cart') 


def orderComplete(request):
    return render(request,'order_complete.html')

def placeOrder(request):
    print(request.POST)
    cart_items = None
    tax = 0
    total = 0
    grand_total = 0
    cart_items = CartItem.objects.filter(user = request.user)
    if cart_items.count() < 1:
        return redirect('store')
    for item in cart_items: 
        total += item.product.price * item.quantity
    print(cart_items)  
    tax = (5*total)/100
    grand_total = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.order_total = grand_total
            form .instance.tax = tax
            form.instance.ip = request.META.get('REMOTE_ADDR')
            saved_instance = form.save()
            form.instance.order_number = saved_instance.id
            form.save()
            print(form)
            return redirect(sslcommerz_payment_gateway(request,  saved_instance.id, str(request.user.id), grand_total))
    return render(request,'place_order.html',{'cart_items' : cart_items, 'tax' : tax,'total' : total, 'grand_total' : grand_total})
