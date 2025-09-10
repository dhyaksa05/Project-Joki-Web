from django.contrib import admin
from .models import Produk, Spesifikasi


class ProdukAdmin(admin.ModelAdmin):
    list_display = ("nama", "kategori", "harga", "kegunaan", "image_path")
    search_fields = ("nama", "kategori", "kegunaan")
    list_filter = ("kategori", "kegunaan")


class SpesifikasiInline(admin.TabularInline):  # atau admin.StackedInline
    model = Spesifikasi
    extra = 1  # jumlah form kosong default yang ditampilkan


class ProdukAdmin(admin.ModelAdmin):
    list_display = ("nama", "kategori", "harga", "kegunaan", "image_path")
    search_fields = ("nama", "kategori", "kegunaan")
    list_filter = ("kategori", "kegunaan")
    inlines = [SpesifikasiInline]  # tambahkan inline di sini


admin.site.register(Produk, ProdukAdmin)
admin.site.register(Spesifikasi)  # optional: supaya bisa diakses juga terpisah

# Register your models here.
