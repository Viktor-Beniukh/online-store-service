from django.conf import settings
from django.db import models

from product.models import Product


class Order(models.Model):
    ORDERED = "Ordered"
    SHIPPED = "Shipped"

    PENDING = "Pending"
    PAID = "Paid"
    CANCELLED = "Cancelled"

    STATUS_PAYMENT = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (CANCELLED, "Cancelled"),
    ]

    STATUS_CHOICES = (
        (ORDERED, "Ordered"),
        (SHIPPED, "Shipped")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
    )
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    zipcode = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    status_order = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=ORDERED
    )
    status_payment = models.CharField(
        max_length=10, choices=STATUS_PAYMENT, default=PENDING
    )
    session_url = models.URLField(max_length=500, blank=True)
    session_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.id)
