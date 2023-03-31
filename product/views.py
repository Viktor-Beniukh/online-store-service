from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from cart.forms import CartAddProductForm

from product.forms import ProductForm
from product.models import Category, Product, Review


def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("query", "")

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {
        "category": category,
        "categories": categories,
        "products": products,
        "page_obj": page_obj,
    }

    return render(
        request, "product/product_list.html", context=context
    )


def product_detail(request, pk, slug):
    product = get_object_or_404(
        Product, pk=pk, slug=slug, is_available=True,
    )
    cart_product_form = CartAddProductForm()

    if request.method == "POST":
        rating = request.POST.get("rating", 3)
        content = request.POST.get("content", "")

        if content:
            reviews = Review.objects.filter(
                created_by=request.user, product=product
            )

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )

            return redirect(
                "product:product-detail", id=product.id, slug=product.slug
            )

    context = {
        "product": product,
        "cart_product_form": cart_product_form,
    }

    return render(
        request, "product/product_detail.html", context=context
    )


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    template_name = "product/category_form.html"
    fields = "__all__"
    success_url = reverse_lazy("product:product-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = "product/category_form.html"
    fields = "__all__"
    slug_url_kwarg = "category_slug"
    success_url = reverse_lazy("product:product-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    slug_url_kwarg = "category_slug"
    success_url = reverse_lazy("product:product-list")


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    template_name = "product/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("product:product-list")


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    template_name = "product/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("product:product-list")


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("product:product-list")
