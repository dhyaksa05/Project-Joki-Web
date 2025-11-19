from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Produk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scrapper_app.scrape_tokopedia import scrape_query,scrape_for_django


def home(request):
    return render(request, "index.html")


def processor(request):
    # ambil hanya produk yang kegunaannya Processor
    produk_list = Produk.objects.filter(kegunaan="Processor")

    context = {"produk_list": produk_list}
    return render(request, "processor.html", context)


def processor_detail(request, slug):
    produk = get_object_or_404(Produk, slug=slug)
    return render(request, "details/processor/index.html", {"produk": produk})


def ram(request):
    return render(request, "ram.html")


def vga(request):
    return render(request, "vga.html")


def psu(request):
    return render(request, "psu.html")


def ssd(request):
    return render(request, "ssd.html")


def rekomendasi_view(request):
    results = []
    scraped_results = []  # Tambahkan ini untuk menyimpan data scraping
    budget = ""
    usage = ""
    custom_usage = ""
    komponen = []

    if request.method == "POST":
        budget = request.POST.get("budget")
        usage = request.POST.get("usage")
        custom_usage = request.POST.get("custom_usage", "")
        komponen = request.POST.getlist("components")

        # gabungkan semua untuk jadi keyword pencarian di Tokopedia
        query_text = (usage or "") + " " + custom_usage + " " + " ".join(komponen)

        # === 1️⃣ Jalankan scraper Tokopedia ===
        try:
            # from scrapper_app.scraper_tokped import scrape_query
            scraped_data = scrape_for_django(query_text)
            # Simpan data scraping ke variabel yang akan dikirim ke template
            scraped_results = scraped_data
        except Exception as e:
            scraped_data = []
            scraped_results = []
            print("❌ Gagal scraping Tokopedia:", e)

        # === 2️⃣ Lanjut ke sistem rekomendasi lokal (Produk di database) ===
        if komponen:
            hardware_qs = Produk.objects.filter(harga__lte=budget, kategori__in=komponen)
        else:
            hardware_qs = Produk.objects.filter(harga__lte=budget)

        if hardware_qs.exists():
            documents = [h.deskripsi for h in hardware_qs]
            documents.append(query_text)

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(documents)
            cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            scores = cosine_sim[0]

            THRESHOLD = 0.15
            ranked_idx = np.argsort(scores)[::-1]

            results = [hardware_qs[int(i)] for i in ranked_idx if scores[i] >= THRESHOLD]

    # Tambahkan scraped_results ke context
    return render(request, 'hasil.html', {
        'results': results,
        'scraped_results': scraped_results,  # Kirim data scraping ke template
        'budget': budget,
        'usage': usage,
        'custom_usage': custom_usage,
        'komponen': komponen,
    })