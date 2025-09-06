
# 🔍 Sistem Rekomendasi Perangkat Keras Komputer (Django)

Proyek ini adalah web application berbasis **Django** untuk memberikan rekomendasi perangkat keras komputer (CPU, GPU, RAM, dll.) sesuai **budget**, **kegunaan**, dan **input kebutuhan spesifik (free text)** menggunakan **Content-Based Filtering** dengan algoritma **TF-IDF** dan **Cosine Similarity**.

## 🚀 Fitur Utama
- ✅ Input budget, kegunaan (gaming, office, design, programming).
- ✅ Checkbox untuk memilih komponen (Processor, VGA, RAM, dll.).
- ✅ Input bebas (free text) seperti *"digunakan untuk bermain game FPS berat"*.
- ✅ Rekomendasi hardware berbasis deskripsi produk menggunakan **TF-IDF + Cosine Similarity**.
- ✅ Tampilan modern menggunakan **Tailwind CSS**.
- ✅ Admin panel untuk input data hardware.

## 🛠️ Teknologi
- **Python 3**
- **Django 5**
- **SQLite (default)**
- **scikit-learn** (TF-IDF, Cosine Similarity)
- **Tailwind CSS**

## 📂 Struktur Project
```
hardware/
│── core/
│   ├── models.py      # Model Produk/Hardware
│   ├── views.py       # View rekomendasi TF-IDF
│   ├── urls.py        # Routing app
│   ├── templates/     # Template index & hasil rekomendasi
│
│── hardware/
│   ├── settings.py
│   ├── urls.py
│
│── db.sqlite3
│── manage.py
```

## ⚙️ Instalasi & Setup
1. **Clone / Download project**
   ```bash
   git clone <repo-url>
   cd hardware
   ```

2. **Buat virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Migrasi database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Buat superuser untuk admin**
   ```bash
   python manage.py createsuperuser
   ```

5. **Jalankan server**
   ```bash
   python manage.py runserver
   ```

6. **Akses aplikasi**
   - Frontend: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📊 Contoh Input Data Produk
Masukkan data di admin panel **Produk**:
- Nama: Intel Core i5 12400F
- Kategori: processor
- Harga: 2500000
- Deskripsi: "Prosesor 6-core cocok untuk bermain game FPS berat"
- Kegunaan: gaming

## 📌 Cara Kerja Rekomendasi
1. User isi budget, pilih komponen, dan masukkan kebutuhan spesifik.
2. Sistem mengambil semua deskripsi produk dari database sesuai filter.
3. Menggunakan **TF-IDF Vectorizer** untuk mengubah teks jadi vektor.
4. Menghitung **Cosine Similarity** antara input user dengan deskripsi produk.
5. Menampilkan rekomendasi dengan similarity tertinggi.

## 📜 Lisensi
Proyek ini dibuat untuk tujuan pembelajaran dan pengembangan sistem rekomendasi berbasis Django.
