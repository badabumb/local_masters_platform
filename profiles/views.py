import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from products.models import Product
from .forms import ProfileForm
from .models import Profile

logger = logging.getLogger("app")


@login_required
def profile_detail(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.first_name},
    )
    products = Product.objects.filter(author=request.user).order_by('-created_at')
    logger.info(
        "Profile page opened",
        extra={
            "path": request.path,
            "method": request.method,
            "request_id": getattr(request, "request_id", None),
        },
    )

    return render(request, "profiles/profile_detail.html", {"profile": profile, "products": products})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/profile_form.html", {"form": form})
