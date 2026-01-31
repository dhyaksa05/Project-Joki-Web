from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
from .models import Produk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scrapper_app.scrape_tokopedia import scrape_query, scrape_for_django
import json
import os
from django.conf import settings
import subprocess
import sys
import urllib.parse
import re
from .utils import text_preprocessing 

def home(request): return render(request, "index.html")
def processor(request): return render(request, "processor.html", {"produk_list": Produk.objects.filter(kegunaan="Processor")})
def processor_detail(request, slug): return render(request, "details/processor/index.html", {"produk": get_object_or_404(Produk, slug=slug)})
def ram(request): return render(request, "ram.html")
def vga(request): return render(request, "vga.html")
def psu(request): return render(request, "psu.html")
def ssd(request): return render(request, "ssd.html")

# === 1. FUNGSI LOAD DATA (FIX LINK & GAMBAR) ===
def load_tokopedia_data(product_type="all"):
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tokopedia_products_latest.json')
        if not os.path.exists(json_path): return []
        with open(json_path, 'r', encoding='utf-8') as f: data = json.load(f)
        products = data if isinstance(data, list) else data.get('products', [])
        
        clean_products = []
        for p in products:
            product_name = p.get('name', 'Produk')
            
            # Fix Link
            raw_link = p.get('link', '').strip()
            if not raw_link or raw_link == '#' or len(raw_link) < 5:
                encoded_name = urllib.parse.quote(product_name)
                p['link'] = f"https://www.tokopedia.com/search?st=product&q={encoded_name}"
            elif raw_link.startswith('https://www.tokopedia.com'): p['link'] = raw_link
            elif raw_link.startswith('/'): p['link'] = f"https://www.tokopedia.com{raw_link}"
            elif raw_link.startswith('tokopedia.com'): p['link'] = f"https://{raw_link}"
            else:
                if not raw_link.startswith('http'): p['link'] = f"https://{raw_link}"

            # Fix Image
            raw_img = p.get('image', '')
            if raw_img and raw_img.startswith('//'): p['image'] = f"https:{raw_img}"
            
            # Fix Harga
            raw_price = str(p.get('price', '0'))
            p['price_int'] = int(re.sub(r'\D', '', raw_price))
            
            clean_products.append(p)

        if product_type != "all":
            clean_products = [p for p in clean_products if p.get('product_type') == product_type]
        
        return clean_products
    except: return []

# === 2. FUNGSI FILTER (STRICT) ===
def filter_products_by_criteria(products, product_type, min_budget=None, max_budget=None, usage=None, components=None):
    if not products: return []
    filtered_products = []

    if product_type == "laptop":
        base_filtered = [
            p for p in products 
            if any(x in p.get('name', '').lower() for x in ['laptop', 'notebook', 'macbook', 'asus', 'acer', 'lenovo', 'hp ', 'dell', 'msi', 'axioo', 'infinix', 'advan'])
            and not any(x in p.get('name', '').lower() for x in ['tas', 'bag', 'case', 'skin', 'keyboard', 'baterai', 'battery', 'charger', 'adaptor', 'fan', 'cooler', 'rakitan', 'pc'])
        ]
        filtered_products = base_filtered
        if usage:
            usage_keywords = {
                "Gaming": ["rtx", "gtx", "gpu", "nvidia", "rog", "tuf", "legion", "nitro", "victus", "predator"],
                "Office/Kerja": ["vivobook", "thinkpad", "latitude", "aspire", "ideapad", "infinix", "advan", "matebook"],
                "Design/Video Editing": ["creator", "oled", "render", "studio", "srgb", "macbook", "proart"],
                "Programming": ["thinkpad", "macbook", "probook", "latitude", "xps", "spectre", "elitebook"]
            }
            if usage in usage_keywords:
                keywords = usage_keywords[usage]
                filtered_products = [p for p in base_filtered if any(k.lower() in p.get('name', '').lower() for k in keywords)]

    elif product_type == "pc_component" and components:
        include_map = {
            "RAM": ["ram ", "ddr4", "ddr5", "sodimm", "dimm", "pc12800", "3200mhz", "2666mhz", "memory"],
            "GPU": ["rtx", "gtx", "rx ", "radeon", "geforce", "graphics card", "vga card"],
            "CPU": ["ryzen", "core i3", "core i5", "core i7", "core i9", "athlon", "pentium", "lga", "am4"],
            "Motherboard": ["motherboard", "mainboard", "mobo", "b450", "b550", "a320", "z790", "h610"],
            "SSD": ["ssd", "nvme", "m.2", "sata3"],
            "HDD": ["hdd", "hardisk", "hard disk", "seagate", "wd blue"],
            "PSU": ["psu", "power supply", "watt", "80+"],
            "Casing": ["casing", "chassis", "case pc", "gaming case"]
        }
        exclude_map = {
            "RAM": ["rakitan", "pc gaming", "laptop", "notebook", "vga", "motherboard", "mobo", "paket"],
            "GPU": ["rakitan", "pc gaming", "laptop", "notebook", "cpu", "ram", "motherboard"],
            "CPU": ["rakitan", "pc gaming", "laptop", "notebook", "vga", "motherboard", "fan"],
            "Motherboard": ["rakitan", "pc gaming", "laptop", "notebook"],
            "SSD": ["rakitan", "pc gaming", "laptop", "notebook", "enclosure"],
            "HDD": ["rakitan", "pc gaming", "laptop", "notebook", "enclosure", "caddy"],
            "PSU": ["rakitan", "pc gaming", "laptop", "notebook", "casing"],
            "Casing": ["rakitan", "pc gaming", "laptop", "notebook", "fan"]
        }

        for p in products:
            name_lower = p.get('name', '').lower()
            is_match = False
            for user_comp in components: 
                target_key = next((k for k in include_map if k.lower() in user_comp.lower()), None)
                if target_key:
                    has_inc = any(ik in name_lower for ik in include_map[target_key])
                    has_exc = any(ek in name_lower for ek in exclude_map.get(target_key, []))
                    if has_inc and not has_exc:
                        is_match = True
                        break 
            if is_match: filtered_products.append(p)
    else: filtered_products = products

    final_results = []
    if min_budget is not None and max_budget is not None:
        try:
            min_b, max_b = int(min_budget), int(max_budget)
            if min_b == max_b: min_b, max_b = int(min_b * 0.7), int(max_b * 1.3)
            final_results = [p for p in filtered_products if min_b <= p['price_int'] <= max_b]
            if not final_results and filtered_products:
                final_results = [p for p in filtered_products if int(min_b*0.5) <= p['price_int'] <= int(max_b*1.5)]
            if not final_results and filtered_products:
                filtered_products.sort(key=lambda x: x['price_int'])
                final_results = filtered_products[:12]
        except: final_results = filtered_products
    else: final_results = filtered_products
    
    return final_results if final_results else products[:10]

def determine_level(price, budget):
    if not budget or budget == 0: return "Standard", "bg-slate-500", "standard"
    ratio = price / budget
    if 0.85 <= ratio <= 1.15: return "⭐ Recommended", "bg-violet-600", "best"
    elif ratio < 0.85: return "💰 Budget Friendly", "bg-emerald-600", "budget"
    elif ratio > 1.15: return "🚀 High Performance", "bg-rose-600", "high"
    return "Standard", "bg-slate-500", "standard"

# === 3. FUNGSI UTAMA + EVALUASI MODEL ===
def process_recommendation(request, data_type, page_type):
    min_budget = request.POST.get("min_budget", "0")
    max_budget = request.POST.get("max_budget", "0")
    budget = request.POST.get("budget", "0")
    usage = request.POST.get("usage", "")
    components = request.POST.getlist("components", [])
    
    try:
        if page_type == 'laptop':
            b_int = int(budget)
            min_b, max_b = int(b_int * 0.7), int(b_int * 1.3)
            target = b_int
        else:
            min_b, max_b = int(min_budget), int(max_budget)
            target = (min_b + max_b) / 2
    except: min_b, max_b, target = 0, 0, 0

    all_data = load_tokopedia_data(data_type)
    raw_recs = filter_products_by_criteria(all_data, data_type, min_b, max_b, usage, components)
    
    grouped_recs = {'best': [], 'high': [], 'budget': [], 'standard': []}
    chart_labels, chart_scores = [], []
    has_data = False

    # --- VARIABEL EVALUASI MODEL ---
    eval_metrics = {
        'total_scanned': len(all_data), # Total data scraping
        'total_filtered': len(raw_recs), # Data yang lolos filter
        'precision_score': 0, # Presisi algoritma
        'avg_similarity': 0, # Rata-rata kemiripan
        'relevant_items': 0 # Item yang dianggap relevan (>10% match)
    }

    if raw_recs:
        docs = [text_preprocessing(p.get('name', '')) for p in raw_recs]
        query = text_preprocessing((usage or "") + " " + " ".join(components))
        docs.append(query)
        
        try:
            vec = TfidfVectorizer()
            matrix = vec.fit_transform(docs)
            scores = cosine_similarity(matrix[-1], matrix[:-1])[0]

            relevant_count = 0
            total_score = 0

            for i, p in enumerate(raw_recs):
                score_val = round(scores[i] * 100, 2)
                p['similarity_score'] = score_val
                
                # Hitung untuk Evaluasi
                total_score += score_val
                if score_val > 10.0: # Threshold Relevansi 10%
                    relevant_count += 1

                lvl_name, lvl_class, lvl_key = determine_level(p.get('price_int', 0), target)
                p['level_name'] = lvl_name
                p['level_class'] = lvl_class
                
                if lvl_key in grouped_recs: grouped_recs[lvl_key].append(p)
                else: grouped_recs['standard'].append(p)

                if len(chart_labels) < 10:
                    chart_labels.append(p.get('name', '')[:20] + "...")
                    chart_scores.append(p['similarity_score'])
            
            # --- HITUNG METRIK FINAL ---
            eval_metrics['relevant_items'] = relevant_count
            if len(raw_recs) > 0:
                eval_metrics['precision_score'] = round((relevant_count / len(raw_recs)) * 100, 2)
                eval_metrics['avg_similarity'] = round(total_score / len(raw_recs), 2)
            
            for k in grouped_recs:
                grouped_recs[k].sort(key=lambda x: x['similarity_score'], reverse=True)
                if grouped_recs[k]: has_data = True
        except: pass

    context = {
        'grouped_recs': grouped_recs,
        'eval_metrics': eval_metrics, # Kirim data evaluasi ke HTML
        'product_type': page_type,
        'min_budget': min_budget, 'max_budget': max_budget, 'budget': budget, 'usage': usage,
        'chart_labels': json.dumps(chart_labels), 'chart_scores': json.dumps(chart_scores),
        'show_chart': has_data,
        'page_title': f"Rekomendasi {page_type.title()}"
    }
    return render(request, 'hasil.html', context)

def rekomendasi_pc_view(request): return process_recommendation(request, "pc_component", "pc")
def rekomendasi_laptop_view(request): return process_recommendation(request, "laptop", "laptop")

def rekomendasi_view(request):
    if request.method == "POST":
        if 'min_budget' in request.POST: return rekomendasi_pc_view(request)
        return rekomendasi_laptop_view(request)
    return render(request, 'rekomendasi_laptop.html')

def run_scraper(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, os.path.join(base_dir, 'scrapper.py')])
    return HttpResponse("✅ Scraper Jalan")

def download_excel(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'tokopedia_products_latest.xlsx')
    if os.path.exists(file_path): return FileResponse(open(file_path, "rb"), as_attachment=True, filename="data.xlsx")
    return JsonResponse({"status": "error"})

def pelajarilebihlanjut(request): return render(request, "pelajarilebihlanjut.html")
def loginpage(request): return render(request, "loginpage.html")
def serve_local_image(request): return Http404("Not used")