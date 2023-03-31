from decimal import Decimal
from django.conf import settings

from product.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initializing the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add the product to the cart or update its quantity.
        """
        product_id = str(product.id)
        product_char = {
            "quantity": 0,
            "price": str(product.price)
        }

        if product_id not in self.cart:
            self.cart[product_id] = product_char

        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        """Refresh the cart session."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """Removing the product from the cart."""
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Search for items in the shopping cart
        and retrieve products from the database.
        """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Counting the number of products in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Calculating the cost of the products in the cart."""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def get_total_items(self):
        """Calculating the number of the products in the cart."""
        return sum(
            item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """Removing the cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
