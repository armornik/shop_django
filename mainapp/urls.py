from django.urls import path
from django.views.decorators.cache import cache_page

from .views import products, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('product/<int:pk>/', cache_page(3600) (product), name='product'),
]
