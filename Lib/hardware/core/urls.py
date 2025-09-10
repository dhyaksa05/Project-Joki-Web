from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('processor/', views.processor, name='processor'),
    path('ram/', views.ram, name='ram'),
    path('vga/', views.vga, name='vga'),
    path('psu/', views.psu, name='psu'),
    path('ssd/', views.ssd, name='ssd'),
    path('rekomendasi/', views.rekomendasi_view, name='rekomendasi'),
]
