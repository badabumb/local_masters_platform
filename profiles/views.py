import logging

from django.shortcuts import render

logger = logging.getLogger("app")


def profile_detail(request):
    profile = {
        "name": "Юлия",
        "city": "Москва",
        "is_master": True,
        "about": "Создаю изделия ручной работы из глины.",
    }

    logger.info(
        "Profile page opened",
        extra={
            "path": request.path,
            "method": request.method,
            "request_id": getattr(request, "request_id", None),
        },
    )

    return render(request, "profiles/profile_detail.html", {"profile": profile})
