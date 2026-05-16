from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product

from .models import CartItem, Order, OrderItem


def _cart_items(user):
    return CartItem.objects.filter(user=user).select_related('product', 'product__author')


def _cart_total(items):
    return sum(item.total_price for item in items)


def _can_add_to_cart(user, product):
    return not product.author_id or product.author_id != user.id


def cart_view(request):
    if request.user.is_authenticated:
        items = list(_cart_items(request.user))
        total = _cart_total(items)
    else:
        items = []
        total = 0
    return render(request, 'orders/cart.html', {'items': items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not _can_add_to_cart(request.user, product):
        messages.warning(request, 'Это ваш товар. Его нельзя добавить в корзину.')
        return redirect('product_detail', pk=product.pk)

    quantity = 1
    if request.method == 'POST':
        try:
            quantity = max(1, int(request.POST.get('quantity', 1)))
        except (TypeError, ValueError):
            quantity = 1

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity},
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=['quantity'])

    messages.success(request, 'Товар добавлен в корзину.')
    return redirect('cart')


@login_required
def increase_cart_item(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not _can_add_to_cart(request.user, product):
        messages.warning(request, 'Это ваш товар. Его нельзя добавить в корзину.')
        return redirect('product_detail', pk=product.pk)

    cart_item, _ = CartItem.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 0})
    cart_item.quantity += 1
    cart_item.save(update_fields=['quantity'])
    return redirect('cart')


@login_required
def decrease_cart_item(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    cart_item.quantity -= 1
    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save(update_fields=['quantity'])
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    messages.info(request, 'Товар удален из корзины.')
    return redirect('cart')


@login_required
def checkout(request):
    items = list(_cart_items(request.user))
    total = _cart_total(items)

    if not items:
        messages.warning(request, 'Корзина пуста.')
        return redirect('cart')

    own_items = [item for item in items if item.product.author_id == request.user.id]
    if own_items:
        CartItem.objects.filter(id__in=[item.id for item in own_items]).delete()
        messages.warning(request, 'Из корзины удалены ваши товары. Их нельзя оформить в заказ.')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total)
        for item in items:
            product = item.product
            OrderItem.objects.create(
                order=order,
                product=product,
                product_title=product.title,
                price=product.price,
                quantity=item.quantity,
            )
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, f'Заказ #{order.pk} оформлен.')
        return redirect('order_list')

    return render(request, 'orders/checkout.html', {'items': items, 'total': total})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_list.html', {'orders': orders})
