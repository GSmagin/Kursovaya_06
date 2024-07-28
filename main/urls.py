from django.urls import path
from .apps import MainConfig
from .views import index, contacts, not_found

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='main'),
    path('contacts/', contacts, name='contacts'),
    path('not_found/', not_found, name='not_found'),
]
