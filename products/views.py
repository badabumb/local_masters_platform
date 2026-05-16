import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Product
from .services import get_all_products

logger = logging.getLogger("app")


def product_list(request):
    products = get_all_products()

    logger.info(
        "Products page opened",
        extra={
            "path": request.path,
            "method": request.method,
            "request_id": getattr(request, "request_id", None),
        },
    )

    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('author'), pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            messages.success(request, 'Товар добавлен.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {"form": form})
