from django.shortcuts import render, get_object_or_404
from .models import Product, Category


#  Product List
def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    #  Search
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    #  Category filter (NEW)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })


#  Product Detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)

    return render(request, 'products/product_detail.html', {
        'product': product
    })