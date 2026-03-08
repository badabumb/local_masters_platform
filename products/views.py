from django.shortcuts import render


def product_list(request):
    products = [
        {'title': 'Ваза из глины', 'price': 1500},
        {'title': 'Серьги ручной работы', 'price': 900},
        {'title': 'Свеча из воска', 'price': 700},
    ]
    return render(request, 'products/product_list.html', {'products': products})
