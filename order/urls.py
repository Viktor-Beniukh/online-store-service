from django.urls import path

from order.views import order_create, my_orders

app_name = "order"


urlpatterns = [
    path("order-create/", order_create, name="order-create"),
    path("order-show/", my_orders, name="order-list"),
]
