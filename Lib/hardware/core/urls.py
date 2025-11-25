from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("processor/", views.processor, name="processor"),
    path(
        "details/processor/<slug:slug>/",
        views.processor_detail,
        name="processor_detail",
    ),
    path("ram/", views.ram, name="ram"),
    path("vga/", views.vga, name="vga"),
    path("psu/", views.psu, name="psu"),
    path("ssd/", views.ssd, name="ssd"),
    path("rekomendasi/", views.rekomendasi_view, name="rekomendasi"),
<<<<<<< HEAD
    path('run-scraper/', views.run_scraper, name='run_scraper'),
    path('download-excel/', views.download_excel, name='download_excel'),
=======
    path("pelajarilebihlanjut/", views.pelajarilebihlanjut, name="pelajarilebihlanjut"),
>>>>>>> 5d3c67796c229d917597e7b83307adbe00f6b259
]
