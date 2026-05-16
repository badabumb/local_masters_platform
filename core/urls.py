from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from pages.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', include('products.urls')),
    path('profile/', include('profiles.urls')),
    path('', include('orders.urls')),
    path('accounts/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
