import logging

from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger("app")


def home(request):
    logger.info(
        "Home page opened",
        extra={
            "path": request.path,
            "method": request.method,
            "request_id": getattr(request, "request_id", None),
        },
    )

    context = {
        "app_version": settings.APP_VERSION,
        "app_env": settings.APP_ENV,
    }
    return render(request, "pages/home.html", context)
