from django.db import models

class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=50, default='Umum')       # default kategori
    deskripsi = models.TextField(default='Belum ada deskripsi')       # default deskripsi
    kegunaan = models.CharField(max_length=100, default='Umum')       # default kegunaan

    def __str__(self):
        return f"{self.nama} ({self.kategori})"
