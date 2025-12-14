from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Produk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scrapper_app.scrape_tokopedia import scrape_query,scrape_for_django
import json
import os
from django.conf import settings
import subprocess
from django.shortcuts import render
import sys


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

def load_tokopedia_data(product_type="all"):
    """
    Load data dari file JSON di folder data
    product_type: 'pc_component', 'laptop', atau 'all'
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
        
        # Filter berdasarkan product_type jika bukan 'all'
        if product_type != "all":
            products = [p for p in products if p.get('product_type') == product_type]
        
        print(f"✅ Loaded {len(products)} {product_type} products from JSON")
        return products
        
    except Exception as e:
        print(f"❌ Error loading JSON data: {e}")
        return []

def filter_products_by_criteria(products, product_type, min_budget=None, max_budget=None, usage=None, components=None):
    """
    Filter produk berdasarkan kriteria
    """
    if not products:
        return []
    
    filtered_products = []
    
    # Filter berdasarkan budget jika diisi
    if min_budget is not None and max_budget is not None:
        try:
            min_budget = int(min_budget)
            max_budget = int(max_budget)
            print(f"💰 Filtering with budget range: Rp {min_budget:,} - {max_budget:,}")
            
            for product in products:
                price = product.get('price', 0)
                if isinstance(price, (int, float)) and min_budget <= price <= max_budget:
                    filtered_products.append(product)
        except (ValueError, TypeError):
            filtered_products = products
    else:
        filtered_products = products
    
    print(f"📊 After budget filter: {len(filtered_products)} products")
    
    # Filter berdasarkan usage/kegunaan (jika produk laptop)
    if product_type == "laptop" and usage:
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
                if any(keyword.lower() in product_name for keyword in keywords):
                    usage_filtered.append(product)
            
            filtered_products = usage_filtered
            print(f"🎯 After usage filter '{usage}': {len(filtered_products)} products")
    
    # Filter berdasarkan komponen (jika produk PC component)
    if product_type == "pc_component" and components:
        components_lower = [c.lower() for c in components]
        components_filtered = []
        
        # Mapping komponen PC
        pc_components_keywords = {
            "CPU": ["cpu", "processor", "intel", "amd", "ryzen", "core i"],
            "GPU": ["gpu", "vga", "graphic card", "nvidia", "geforce", "rtx", "gtx", "radeon"],
            "RAM": ["ram", "memory", "ddr4", "ddr5"],
            "Motherboard": ["motherboard", "mainboard", "mobo"],
            "SSD": ["ssd", "nvme", "solid state"],
            "HDD": ["hdd", "hard disk"],
            "PSU": ["psu", "power supply"],
            "Casing": ["casing", "case", "chassis"]
        }
        
        for product in filtered_products:
            product_name = product.get('name', '').lower()
            component_type = product.get('component_type', '').lower()
            
            # Cek berdasarkan nama komponen atau tipe komponen
            for comp in components_lower:
                if comp in pc_components_keywords:
                    keywords = pc_components_keywords[comp]
                    if any(keyword in product_name for keyword in keywords):
                        components_filtered.append(product)
                        break
                elif comp == component_type:
                    components_filtered.append(product)
                    break
        
        # Hapus duplikat
        components_filtered = list({p['id']: p for p in components_filtered}.values())
        filtered_products = components_filtered
        print(f"🔧 After components filter: {len(filtered_products)} products")
    
    # Urutkan berdasarkan rating dan review count
    filtered_products.sort(key=lambda x: (
        x.get('rating', 0) or 0, 
        x.get('review_count', 0) or 0,
        -(x.get('price', 0))
    ), reverse=True)
    
    return filtered_products[:15]  # Return top 15
def rekomendasi_pc_view(request):
    """
    View untuk rekomendasi PC components
    """
    results = []
    json_recommendations = []
    min_budget = ""
    max_budget = ""
    usage = ""
    components = []
    page_title = "Rekomendasi Komponen PC"
    product_type = "pc"
    
    if request.method == "POST":
        min_budget = request.POST.get("min_budget", "")
        max_budget = request.POST.get("max_budget", "")
        usage = request.POST.get("usage", "")
        components = request.POST.getlist("components", [])
        
        print(f"🎯 PC Request: min_budget={min_budget}, max_budget={max_budget}, usage={usage}, components={components}")
        
        # === 1️⃣ Dapatkan rekomendasi dari data JSON (PC components) ===
        if min_budget and max_budget:
            try:
                min_budget_int = int(min_budget)
                max_budget_int = int(max_budget)
                all_components = load_tokopedia_data("pc_component")
                json_recommendations = filter_products_by_criteria(
                    all_components, 
                    "pc_component", 
                    min_budget_int, 
                    max_budget_int, 
                    usage, 
                    components
                )
                print(f"✅ PC JSON recommendations: {len(json_recommendations)} products")
            except (ValueError, TypeError) as e:
                print(f"❌ Error parsing budget: {e}")
        else:
            print("⚠️ Budget tidak lengkap, skip filtering JSON")
        
        # === 2️⃣ Sistem rekomendasi lokal (Produk PC di database) ===
        try:
            if min_budget and max_budget and components:
                # Filter untuk komponen PC di database lokal
                hardware_qs = Produk.objects.filter(
                    harga__gte=min_budget,
                    harga__lte=max_budget,
                    kategori__in=components
                )
            elif min_budget and max_budget:
                hardware_qs = Produk.objects.filter(
                    harga__gte=min_budget,
                    harga__lte=max_budget
                )
            else:
                hardware_qs = Produk.objects.none()
            
            if hardware_qs.exists():
                # Gabungkan semua untuk jadi keyword pencarian
                query_text = (usage or "") + " " + " ".join(components)
                
                documents = [h.deskripsi for h in hardware_qs]
                documents.append(query_text)
                
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(documents)
                cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
                scores = cosine_sim[0]
                
                THRESHOLD = 0.15
                ranked_idx = np.argsort(scores)[::-1]
                
                results = [hardware_qs[int(i)] for i in ranked_idx if scores[i] >= THRESHOLD]
                print(f"✅ PC Database recommendations: {len(results)} products")
                
        except Exception as e:
            print(f"❌ Error in PC local recommendation: {e}")
            results = []
    
    return render(request, 'hasil.html', {
        'results': results,
        'json_recommendations': json_recommendations,
        'budget': f"{min_budget} - {max_budget}" if min_budget and max_budget else "",
        'min_budget': min_budget,
        'max_budget': max_budget,
        'usage': usage,
        'komponen': components,
        'product_type': product_type,
        'page_title': page_title,
    })

def rekomendasi_laptop_view(request):
    """
    View untuk rekomendasi Laptop
    """
    results = []
    json_recommendations = []
    budget = ""
    usage = ""
    custom_usage = ""
    komponen = []
    page_title = "Rekomendasi Laptop"
    product_type = "laptop"
    
    # Variabel untuk budget range
    budget_range_min = 0
    budget_range_max = 0
    
    if request.method == "POST":
        budget = request.POST.get("budget", "")
        usage = request.POST.get("usage", "")
        custom_usage = request.POST.get("custom_usage", "")
        komponen = request.POST.getlist("components", [])
        
        print(f"🎯 Laptop Request: budget={budget}, usage={usage}, komponen={komponen}")
        
        # Hitung budget range untuk ditampilkan di template
        if budget:
            try:
                budget_int = int(budget)
                budget_range_min = int(budget_int * 0.7)
                budget_range_max = int(budget_int * 1.3)
                
                # === Dapatkan rekomendasi dari data JSON (Laptop) ===
                all_laptops = load_tokopedia_data("laptop")
                json_recommendations = filter_products_by_criteria(
                    all_laptops,
                    "laptop",
                    budget_range_min,
                    budget_range_max,
                    usage,
                    None  # Komponen tidak berlaku untuk laptop
                )
                print(f"✅ Laptop JSON recommendations: {len(json_recommendations)} products")
            except (ValueError, TypeError) as e:
                print(f"❌ Error parsing budget: {e}")
        else:
            print("⚠️ Budget tidak diisi, skip filtering JSON")
        
        # === Sistem rekomendasi lokal (Produk Laptop di database) ===
        try:
            if budget:
                budget_int = int(budget)
                min_budget = int(budget_int * 0.7)
                max_budget = int(budget_int * 1.3)
                hardware_qs = Produk.objects.filter(
                    harga__gte=min_budget,
                    harga__lte=max_budget,
                    kategori__icontains="laptop"
                )
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
                print(f"✅ Laptop Database recommendations: {len(results)} products")
                
        except Exception as e:
            print(f"❌ Error in Laptop local recommendation: {e}")
            results = []
    
    return render(request, 'hasil.html', {
        'results': results,
        'json_recommendations': json_recommendations,
        'budget': budget,
        'usage': usage,
        'custom_usage': custom_usage,
        'komponen': komponen,
        'product_type': product_type,
        'page_title': page_title,
        'budget_range_min': budget_range_min,  # Budget range minimum
        'budget_range_max': budget_range_max,  # Budget range maksimum
    })

def rekomendasi_view(request):
    """
    View universal yang menentukan ke mana mengarahkan berdasarkan parameter
    """
    # Cek apakah ada parameter type di URL atau POST
    product_type = request.GET.get('type', '')
    
    if request.method == "POST":
        # Cek berdasarkan form yang dikirim
        if 'min_budget' in request.POST and 'max_budget' in request.POST:
            # Ini dari form PC components
            return rekomendasi_pc_view(request)
        else:
            # Ini dari form Laptop
            return rekomendasi_laptop_view(request)
    else:
        # Jika GET request dengan parameter type
        if product_type == 'pc':
            return render(request, 'rekomendasi_pc.html')
        else:
            return render(request, 'rekomendasi_laptop.html')

def run_scraper(request):
    # Path root project (tempat manage.py berada)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path ke file scrapper.py
    scraper_path = os.path.join(base_dir,'scrapper.py')

    # Gunakan Python dari venv
    python_path = sys.executable

    # Jalankan scraper
    subprocess.run([python_path, scraper_path])

    return HttpResponse("✅ Scraper Tokopedia berhasil dijalankan")

def download_excel(request):
    base_dir = settings.BASE_DIR  # root project
    file_path = os.path.join(base_dir, 'data', 'tokopedia_products_latest.xlsx')

    print("Real path:", file_path)

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename="tokopedia_products_latest.xlsx"
        )
    else:
        return JsonResponse({
            "status": "error",
            "message": f"File tidak ditemukan di: {file_path}"
        })

def pelajarilebihlanjut(request):
    return render(request, "pelajarilebihlanjut.html")

def loginpage(request):
    return render(request, "loginpage.html")
    
