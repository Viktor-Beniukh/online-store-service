import stripe

from django.conf import settings
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from cart.cart import Cart
from order.forms import OrderCreateForm
from order.models import OrderItem, Order
from product.models import Product

BASE_URL = "http://127.0.0.1:8000"
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def my_orders(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user_id=request.user)
    product_ordered = OrderItem.objects.all()

    paginator = Paginator(orders, 5)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {
        "products": products,
        "orders": orders,
        "product_ordered": product_ordered,
        "page_obj": page_obj,
    }

    return render(request, "order/order_list.html", context=context)


def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"]
                )

            cart.clear()

            context = {
                "order": order,
            }

            return render(
                request, "order/order_created.html", context=context
            )

    else:
        form = OrderCreateForm

        context = {
            "cart": cart,
            "form": form,
        }

        return render(request, "order/order_create.html", context=context)


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order = Order.objects.get(id=order_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(order.get_total_cost() * 100),
                        "product_data": {
                            "name": f"Order №{order.id}",
                            "description": "Payment of the order",
                        },
                    },
                    "quantity": 1,
                },
            ],
            metadata={
                "order_id": order.id
            },
            mode="payment",
            success_url=BASE_URL + "/success/",
            cancel_url=BASE_URL + "/cancel/",
        )

        order.session_id = checkout_session.id
        order.session_url = checkout_session.url
        order.save()

        return redirect(order.session_url)


def success(request):
    orders = Order.objects.all()
    for order in orders:
        if order.session_id:
            order.status_payment = Order.PAID
            order.is_paid = True
            order.status_order = Order.SHIPPED
            order.paid_amount = order.get_total_cost()

            order.save()

    return render(request, "order/success.html")


def cancel(request):
    orders = Order.objects.all()

    for order in orders:
        if order.session_id and order.is_paid is False:
            order.status_payment = Order.CANCELLED

            order.save()

    return render(request, "order/cancel.html")
