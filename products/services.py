from .models import Product


def get_all_products():
    return Product.objects.select_related('author').order_by('-created_at')
