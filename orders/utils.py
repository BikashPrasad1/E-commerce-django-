def calculate_cart_total(cart):
    total = 0

    for item in cart.items.all():
        total += item.quantity * item.product.price

    return total