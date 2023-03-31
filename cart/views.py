from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from product.models import Product


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data["quantity"],
            update_quantity=cleaned_data["update"]
        )

    return redirect("cart:cart-detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart-detail")


def cart_detail(request):
    cart = Cart(request)
    context = {
        "cart": cart,
    }

    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "update": True}
        )

    return render(request, "cart/cart_detail.html", context=context)
