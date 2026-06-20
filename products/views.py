import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from profiles.models import Profile
from .forms import ProductForm
from .models import Product
from .services import get_all_products

logger = logging.getLogger("app")


def _is_master(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return False
    return profile.is_master


def _can_edit_product(user, product):
    return user.is_staff or user.is_superuser or product.author_id == user.id


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
    can_edit = request.user.is_authenticated and _can_edit_product(request.user, product)
    return render(request, "products/product_detail.html", {"product": product, "can_edit": can_edit})


@login_required
def product_create(request):
    if not _is_master(request.user):
        messages.error(request, 'Добавлять товары могут только мастера.')
        return redirect('profile_detail')

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


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not _can_edit_product(request.user, product):
        messages.error(request, 'Вы можете редактировать только свои товары.')
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар обновлен.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {"form": form, "product": product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not _can_edit_product(request.user, product):
        messages.error(request, 'Вы можете удалять только свои товары.')
        return redirect('product_detail', pk=product.pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удален.')
        return redirect('product_list')

    return render(request, "products/product_confirm_delete.html", {"product": product})
