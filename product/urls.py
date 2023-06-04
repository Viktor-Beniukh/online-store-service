from django.urls import path

from product.views import (
    product_list,
    product_detail,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = "product"

urlpatterns = [
    path("", product_list, name="product-list"),
    path(
        "<slug:category_slug>/",
        product_list,
        name="product-list-by-category"
    ),
    path(
        "<int:pk>/<slug:slug>/",
        product_detail,
        name="product-detail"
    ),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<slug:category_slug>/update/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<slug:category_slug>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path(
        "<int:id>/<slug:slug>/update/",
        ProductUpdateView.as_view(),
        name="product-update"
    ),
    path(
        "<int:id>/<slug:slug>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete"
    ),
]
