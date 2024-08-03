from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import BlogConfig
from .views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blogpost_list'),
    path('сreate/', BlogCreateView.as_view(), name='blogpost_create'),
    path('detail/<int:pk>/',  cache_page(60)(BlogDetailView.as_view()), name='blogpost_detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blogpost_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blogpost_delete'),
]
