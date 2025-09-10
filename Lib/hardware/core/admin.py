from django.contrib import admin
from .models import Produk


class ProdukAdmin(admin.ModelAdmin):
    list_display = ("nama", "kategori", "harga", "kegunaan", "image_path")
    search_fields = ("nama", "kategori", "kegunaan")
    list_filter = ("kategori", "kegunaan")


admin.site.register(Produk, ProdukAdmin)

# Register your models here.
