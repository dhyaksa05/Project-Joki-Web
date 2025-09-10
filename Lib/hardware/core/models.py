from django.db import models
from django.utils.text import slugify


class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=50, default="Umum")  # default kategori
    deskripsi = models.TextField(default="Belum ada deskripsi")  # default deskripsi
    kegunaan = models.CharField(max_length=100, default="Umum")  # default kegunaan
    image_path = models.CharField(max_length=255, default="images/default.png")
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nama)
            slug = base_slug
            counter = 1
            while Produk.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama} ({self.kategori})"


class Spesifikasi(models.Model):
    nama = models.CharField(max_length=100)
    detail = models.TextField()
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,  # kalau produk dihapus, spesifikasi ikut terhapus
        related_name="spesifikasi",  # supaya bisa diakses lewat produk.spesifikasi.all()
    )

    def __str__(self):
        return f"{self.nama} - {self.produk.nama}"
