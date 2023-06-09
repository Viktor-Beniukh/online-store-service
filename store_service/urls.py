"""store_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import frontpage
from order.views import CreateCheckoutSessionView, success, cancel

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", frontpage, name="frontpage"),
    path("cart/", include("cart.urls", namespace="cart")),
    path("products/", include("product.urls", namespace="products")),
    path("user/", include("user.urls", namespace="user")),
    path("orders/", include("order.urls", namespace="orders")),
    path(
        "<int:pk>/create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session"
    ),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
