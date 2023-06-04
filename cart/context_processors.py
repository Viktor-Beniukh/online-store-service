from cart.cart import Cart


def cart(request):
    cart_processor = {
        "cart": Cart(request)
    }

    return cart_processor
