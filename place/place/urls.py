from django.urls import path, re_path
from django.conf.urls import url
from .views import index, city, get_cat, category, business  # , get_place

urlpatterns = [
    path('', index, name='index'),
    # path('place/<int:pk>', get_place, name='place'), # Access by ID place/id
    path('<str:city_name>/<str:category_name>/<str:business_name>', business, name='business'),
    path('<str:city_name>/<str:category_name>', category, name='category'),
    path('<str:city_name>', city, name='city'),
]
