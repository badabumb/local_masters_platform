from django.shortcuts import render


def profile_detail(request):
    profile = {
        'name': 'Юлия',
        'city': 'Москва',
        'is_master': True,
        'about': 'Создаю изделия ручной работы из глины.',
    }
    return render(request, 'profiles/profile_detail.html', {'profile': profile})
