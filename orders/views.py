from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Cart, CartItem, Order, OrderItem

from django.views.decorators.http import require_POST


#  Get or create cart
def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


#  Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #  Prevent out of stock
    if product.stock <= 0:
        return redirect('product_list')

    cart = get_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1

    item.save()

    return redirect('cart_detail')


#  Cart page
@login_required
def cart_detail(request):
    cart = get_cart(request.user)
    items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in items:
        total_price += item.quantity * item.product.price

    return render(request, 'orders/cart.html', {
        'items': items,
        'total_price': total_price
    })


#  Remove item (SECURE FIX)
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')


#  Checkout
@login_required
def checkout(request):
    cart = get_cart(request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return redirect('product_list')

    total_price = 0
    for item in items:
        total_price += item.quantity * item.product.price

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # Create order items + reduce stock
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart
    items.delete()

    return render(request, 'orders/checkout.html', {'order': order})

@require_POST
@login_required
def update_quantity(request, item_id):
    action = request.POST.get('action')

    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == 'increase':
        item.quantity += 1

    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect('cart_detail')

    item.save()

    return redirect('cart_detail')