# in context_processors.py

from .models import Product

def product_links(request):
    links = Product.objects.all()
    return {'product_links': links}
