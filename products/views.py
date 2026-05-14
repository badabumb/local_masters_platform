import logging

from django.shortcuts import render
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
