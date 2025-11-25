from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Produk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scrapper_app.scrape_tokopedia import scrape_query,scrape_for_django
import json
import os
from django.shortcuts import render

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


def load_tokopedia_data():
    """
    Load data dari file JSON di folder data
    """
    try:
        # Path ke file JSON - sesuaikan dengan struktur project
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tokopedia_products_latest.json')
        json_path = os.path.abspath(json_path)
        
        print(f"📂 Loading data from: {json_path}")
        
        if not os.path.exists(json_path):
            print("❌ File JSON tidak ditemukan")
            return []
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both formats: direct array or with metadata
        if isinstance(data, list):
            products = data
        elif isinstance(data, dict) and 'products' in data:
            products = data['products']
        else:
            products = []
        
        print(f"✅ Loaded {len(products)} products from JSON")
        return products
        
    except Exception as e:
        print(f"❌ Error loading JSON data: {e}")
        return []

def filter_products_by_criteria(products, budget, usage, komponen):
    """
    Filter produk berdasarkan kriteria budget, usage, dan komponen
    """
    if not products:
        return []
    
    try:
        budget = int(budget)
    except (ValueError, TypeError):
        return []
    
    # Filter berdasarkan budget (70% - 130% dari budget)
    budget_min = int(budget * 0.7)
    budget_max = int(budget * 1.3)
    
    print(f"💰 Filtering with budget: Rp {budget:,} (range: {budget_min:,} - {budget_max:,})")
    
    filtered_products = []
    for product in products:
        price = product.get('price', 0)
        if isinstance(price, (int, float)) and budget_min <= price <= budget_max:
            filtered_products.append(product)
    
    print(f"📊 After budget filter: {len(filtered_products)} products")
    
    # Filter berdasarkan usage/kegunaan
    usage_keywords = {
        "Gaming": ["gaming", "game", "rtx", "gtx", "gpu", "graphic", "nvidia", "amd", "rog", "predator", "tuf", "legion"],
        "Office/Kerja": ["office", "kerja", "bisnis", "business", "ultrabook", "thinkpad", "latitude", "elitebook", "vivobook"],
        "Design/Video Editing": ["design", "editing", "video", "creative", "render", "studio", "creator", "workstation"],
        "Programming": ["programming", "developer", "code", "development", "ideapad", "thinkbook"]
    }
    
    if usage in usage_keywords:
        keywords = usage_keywords[usage]
        usage_filtered = []
        for product in filtered_products:
            product_name = product.get('name', '').lower()
            product_category = product.get('category', '').lower()
            
            # Cek di nama produk atau kategori
            if any(keyword.lower() in product_name for keyword in keywords):
                usage_filtered.append(product)
            elif any(keyword.lower() in product_category for keyword in keywords):
                usage_filtered.append(product)
        
        filtered_products = usage_filtered
        print(f"🎯 After usage filter '{usage}': {len(filtered_products)} products")
    
    # Filter berdasarkan komponen
    if komponen:
        komponen_lower = [k.lower() for k in komponen]
        komponen_filtered = []
        
        # Mapping komponen ke keyword
        komponen_keywords = {
            "storage": ["ssd", "hdd", "nvme", "hard disk", "solid state", "storage"],
            "ram": ["ram", "memory", "ddr4", "ddr5", "sodimm"],
            "processor": ["processor", "cpu", "intel", "amd", "ryzen", "core i", "core i3", "core i5", "core i7", "core i9"],
            "gpu": ["gpu", "vga", "graphic card", "nvidia", "geforce", "rtx", "gtx", "radeon"],
            "display": ["display", "monitor", "screen", "ips", "oled", "led", "144hz", "240hz"],
            "battery": ["battery", "baterai", "power", "charging"]
        }
        
        for product in filtered_products:
            product_name = product.get('name', '').lower()
            product_category = product.get('category', '').lower()
            
            # Cek setiap komponen yang dipilih
            for komp in komponen_lower:
                if komp in komponen_keywords:
                    keywords = komponen_keywords[komp]
                    if any(keyword in product_name for keyword in keywords):
                        komponen_filtered.append(product)
                        break
                # Jika komponen tidak ada di mapping, cari langsung
                elif komp in product_name:
                    komponen_filtered.append(product)
                    break
        
        # Hapus duplikat
        komponen_filtered = list({p['id']: p for p in komponen_filtered}.values())
        filtered_products = komponen_filtered
        print(f"🔧 After components filter: {len(filtered_products)} products")
    
    # Urutkan berdasarkan rating dan review count
    filtered_products.sort(key=lambda x: (
        x.get('rating', 0) or 0, 
        x.get('review_count', 0) or 0,
        -(x.get('price', 0))  # Murah ke mahal untuk rating yang sama
    ), reverse=True)
    
    return filtered_products[:20]  # Return top 20

def rekomendasi_view(request):
    results = []
    json_recommendations = []  # Data dari JSON file
    budget = ""
    usage = ""
    custom_usage = ""
    komponen = []

    if request.method == "POST":
        budget = request.POST.get("budget", "")
        usage = request.POST.get("usage", "")
        custom_usage = request.POST.get("custom_usage", "")
        komponen = request.POST.getlist("components", [])

        print(f"🎯 Request: budget={budget}, usage={usage}, komponen={komponen}")

        # === 1️⃣ Dapatkan rekomendasi dari data JSON ===
        if budget:  # Hanya filter jika budget diisi
            all_products = load_tokopedia_data()
            json_recommendations = filter_products_by_criteria(all_products, budget, usage, komponen)
            print(f"✅ JSON recommendations: {len(json_recommendations)} products")
        else:
            print("⚠️  Budget tidak diisi, skip filtering JSON")

        # === 2️⃣ Sistem rekomendasi lokal (Produk di database) ===
        try:
            if budget and komponen:
                hardware_qs = Produk.objects.filter(harga__lte=budget, kategori__in=komponen)
            elif budget:
                hardware_qs = Produk.objects.filter(harga__lte=budget)
            else:
                hardware_qs = Produk.objects.none()

            if hardware_qs.exists():
                # Gabungkan semua untuk jadi keyword pencarian
                query_text = (usage or "") + " " + custom_usage + " " + " ".join(komponen)
                
                documents = [h.deskripsi for h in hardware_qs]
                documents.append(query_text)

                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(documents)
                cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
                scores = cosine_sim[0]

                THRESHOLD = 0.15
                ranked_idx = np.argsort(scores)[::-1]

                results = [hardware_qs[int(i)] for i in ranked_idx if scores[i] >= THRESHOLD]
                print(f"✅ Database recommendations: {len(results)} products")
                
        except Exception as e:
            print(f"❌ Error in local recommendation: {e}")
            results = []

    # Kirim semua data ke template
    return render(request, 'hasil.html', {
        'results': results,
        'json_recommendations': json_recommendations,  # Data dari JSON
        'budget': budget,
        'usage': usage,
        'custom_usage': custom_usage,
        'komponen': komponen,
    })

def pelajarilebihlanjut(request):
    return render(request, "pelajarilebihlanjut.html")

def loginpage(request):
    return render(request, "loginpage.html")
