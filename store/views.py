from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from django.db.models import Q

def store(request,category_slug=None):
    print(category_slug)
    category=None
    products = None
    if category_slug :
        category = get_object_or_404(Category,slug=category_slug)
        products =Product.objects.filter(is_available=True,category=category)
    else:
        products =Product.objects.filter(is_available=True)
        category = Category.objects.all()
    
   
    
    context ={'products':products,'categories':category}
   
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e :
        raise e
    context ={
        'single_product' : single_product
    }  
    return render(request,'details.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'p_count': product_count,
    }
    return render(request, 'store.html', context)
