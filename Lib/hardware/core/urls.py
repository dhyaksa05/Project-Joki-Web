from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('processor/', views.processor, name='processor'),
    path('rekomendasi/', views.rekomendasi_view, name='rekomendasi'),
]
