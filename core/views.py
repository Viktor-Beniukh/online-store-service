from django.core.paginator import Paginator
from django.shortcuts import render

from product.models import Product


def frontpage(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    context = {
        "products": products,
        "page_obj": page_obj,
    }
    return render(request, "core/frontpage.html", context=context)
