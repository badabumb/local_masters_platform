from django.contrib import admin
from django.urls import path
from pages.views import home
from products.views import product_list
from profiles.views import profile_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('profile/', profile_detail, name='profile_detail'),
]
