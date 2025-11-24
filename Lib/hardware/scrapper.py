# save_tokopedia_data.py
import requests
import json
import math
import uuid
from datetime import datetime
import os
from openpyxl import Workbook

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")

os.makedirs(IMAGE_DIR, exist_ok=True)

def safe_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name)

def download_image(url):
    if not url:
        return None

    try:
        # Tentukan ekstensi
        ext = ".jpg"
        u = url.lower()
        if ".png" in u:
            ext = ".png"
        elif ".webp" in u:
            ext = ".webp"
        elif ".jpeg" in u:
            ext = ".jpeg"

        filename = f"{uuid.uuid4().hex}{ext}"

        # ABSOLUTE path untuk menyimpan file
        filepath = os.path.join(IMAGE_DIR, filename)

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.tokopedia.com/"
        }

        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)

            # RETURN RELATIVE PATH
            relative = os.path.join("Lib", "hardware", "data", "images", filename)
            return relative

    except Exception as e:
        print(f"Gagal download image: {e}")

    return None

TOKOPEDIA_API_URL = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"
def parse_price(value):
    """
    Konversi harga dari Tokopedia ke integer.
    Contoh: "Rp1.234.000" → 1234000
    """
    if not value:
        return 0

    try:
        # Pastikan string
        value = str(value)

        # Ambil hanya digit
        digits = ''.join(filter(str.isdigit, value))

        return int(digits) if digits else 0
    except:
        return 0


def search_tokopedia(query: str, price_min: int = None, price_max: int = None, rows: int = 60, page: int = 1):
    """
    Cari produk di Tokopedia menggunakan API internal SearchProductQueryV4.
    """
    # Variabel untuk GraphQL
    params = {
        "device": "desktop",
        "navsource": "home",
        "ob": 23,
        "page": page,
        "q": query,
        "related": True,
        "rows": rows,
        "safe_search": False,
        "scheme": "https",
        "shipping": "",
        "source": "universe",
        "srp_component_id": "01.02.01.01",
        "st": "product",
        "start": (page - 1) * rows,
        "topads_bucket": True,
        "unique_id": "some-unique-id",
        "user_addressId": "",
        "user_cityId": "",
        "user_districtId": "",
        "user_id": "",
        "user_lat": "",
        "user_long": "",
        "user_postCode": "",
        "user_warehouseId": "",
        "variants": ""
    }

    # Tambahkan filter harga
    if price_min is not None or price_max is not None:
        filt = []
        if price_min is not None:
            filt.append(f"price_min={price_min}")
        if price_max is not None:
            filt.append(f"price_max={price_max}")
        param_str = "&".join([f"{k}={v}" for k, v in params.items()] + filt)
    else:
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])

    # Body GraphQL
    graphql_query = {
        "operationName": "SearchProductQueryV4",
        "variables": {"params": param_str},
        "query": """
        query SearchProductQueryV4($params: String!) {
          ace_search_product_v4(params: $params) {
            header {
              totalData
              totalDataText
              processTime
              responseCode
              errorMessage
              additionalParams
              keywordProcess
              componentId
            }
            data {
              products {
                id
                name
                originalPrice
                price
                priceRange
                imageUrl
                rating
                countReview
                url
                shop {
                  name
                  city
                }
                __typename
              }
            }
          }
        }
        """
    }

    headers = {
        "authority": "gql.tokopedia.com",
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://www.tokopedia.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "sec-fetch-site": "same-site",
    }

    try:
        response = requests.post(TOKOPEDIA_API_URL, headers=headers, json=graphql_query)
        response.raise_for_status()
        
        data = response.json()
        products = data.get("data", {}).get("ace_search_product_v4", {}).get("data", {}).get("products", [])
        
        results = []
        for p in products:
            # Konversi harga ke integer dengan handling yang aman
            price = parse_price(p.get("price"))
            
            original_price = parse_price(p.get("originalPrice"))
            if original_price == 0:
                original_price = None
            image_url = p.get("imageUrl")
            local_image = download_image(image_url)
            results.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "price": price,
                "original_price": original_price,
                "image_url": image_url,
                "local_image": local_image,
                "rating": p.get("rating"),
                "review_count": p.get("countReview"),
                "url": p.get("url"),
                "shop_name": p.get("shop", {}).get("name"),
                "shop_city": p.get("shop", {}).get("city"),
                "category": query.lower(),
                "last_updated": datetime.now().isoformat()
            })
        
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def save_products_to_json(products, filename=None):
    """
    Simpan produk ke file JSON
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tokopedia_products_{timestamp}.json"
    
    # Buat directory data jika belum ada
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Data berhasil disimpan ke: {filepath}")
    return filepath

def save_products_to_excel(products, filename="tokopedia_products.xlsx"):
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)

    wb = Workbook()
    ws = wb.active
    ws.title = "Tokopedia Products"

    # Header
    headers = [
        "ID", "Name", "Price", "Original Price", "Rating",
        "Review Count", "Shop", "City", "Image URL", "Local Image", "URL", "Category"
    ]
    ws.append(headers)

    # Data rows
    for p in products:
        ws.append([
            p.get("id"),
            p.get("name"),
            p.get("price"),
            p.get("original_price"),
            p.get("rating"),
            p.get("review_count"),
            p.get("shop_name"),
            p.get("shop_city"),
            p.get("image_url"),
            p.get("local_image"),
            p.get("url"),
            p.get("category")
        ])

    wb.save(filepath)
    print(f"✅ Excel disimpan ke: {filepath}")


def load_products_from_json(filename):
    """
    Load produk dari file JSON
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            products = json.load(f)
            
            # Pastikan harga sudah dalam format integer
            for product in products:
                if isinstance(product.get('price'), str):
                    try:
                        product['price'] = int(product['price'].replace('.', '').replace(',', '').split('.')[0])
                    except (ValueError, TypeError):
                        product['price'] = 0
                
                if isinstance(product.get('original_price'), str):
                    try:
                        product['original_price'] = int(product['original_price'].replace('.', '').replace(',', '').split('.')[0])
                    except (ValueError, TypeError):
                        product['original_price'] = None
            
            return products
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan")
        return []
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

def get_recommendations(budget, usage, required_components=None):
    """
    Dapatkan rekomendasi berdasarkan kriteria
    """
    # Load data dari file JSON terbaru
    data_files = [f for f in os.listdir("data") if f.startswith("tokopedia_products") and f.endswith(".json")]
    if not data_files:
        print("Tidak ada data produk yang ditemukan")
        return []
    
    # Gunakan file terbaru
    latest_file = sorted(data_files)[-1]
    products = load_products_from_json(os.path.join("data", latest_file))
    
    if not products:
        print("Tidak ada produk yang dapat dimuat")
        return []
    
    # Filter berdasarkan budget
    budget_min = budget * 0.8  # 80% dari budget
    budget_max = budget * 1.2  # 120% dari budget
    
    print(f"Budget range: {budget_min} - {budget_max}")
    
    filtered_products = []
    for p in products:
        price = p.get('price')
        if price and isinstance(price, (int, float)):
            if budget_min <= price <= budget_max:
                filtered_products.append(p)
    
    print(f"Produk setelah filter budget: {len(filtered_products)}")
    
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
        for p in filtered_products:
            product_name = p.get('name', '').lower()
            if any(keyword.lower() in product_name for keyword in keywords):
                usage_filtered.append(p)
        
        filtered_products = usage_filtered
        print(f"Produk setelah filter usage '{usage}': {len(filtered_products)}")
    
    # Urutkan berdasarkan rating dan review count
    filtered_products.sort(key=lambda x: (
        x.get('rating', 0) or 0, 
        x.get('review_count', 0) or 0
    ), reverse=True)
    
    # Return top 10 recommendations
    recommendations = filtered_products[:10]
    print(f"Rekomendasi final: {len(recommendations)} produk")
    
    return recommendations

def update_product_data():
    """
    Fungsi untuk update data produk secara berkala
    """
    print("Memulai update data produk...")
    
    queries = [
        ("laptop gaming", 5000000, 20000000),
        ("laptop office", 3000000, 10000000),
        ("laptop programming", 4000000, 15000000),
        ("laptop design", 8000000, 25000000)
    ]
    
    all_products = []
    for query, min_price, max_price in queries:
        print(f"Mengambil data untuk: {query} (Rp {min_price:,} - Rp {max_price:,})")
        products = search_tokopedia(query, price_min=min_price, price_max=max_price, rows=50)
        all_products.extend(products)
        print(f"Berhasil mengambil {len(products)} produk untuk {query}")
    
    filename = save_products_to_json(all_products, "tokopedia_products_latest.json")
    save_products_to_excel(all_products, "tokopedia_products_latest.xlsx")
    
    print(f"\nTotal produk yang berhasil diambil: {len(all_products)}")
    print(f"Data tersimpan di: {filename}")
    
    return all_products

if __name__ == "__main__":
    # Update data produk
    all_products = update_product_data()
    
    # Test recommendations
    print("\n" + "="*50)
    print("TEST REKOMENDASI")
    print("="*50)
    
    test_cases = [
        (8000000, "Gaming"),
        (5000000, "Office/Kerja"),
        (10000000, "Programming"),
        (15000000, "Design/Video Editing")
    ]
    
    for budget, usage in test_cases:
        print(f"\nTesting: Budget Rp {budget:,}, Usage: {usage}")
        recommendations = get_recommendations(budget, usage)
        
        if recommendations:
            print(f"Rekomendasi ditemukan: {len(recommendations)} produk")
            for i, product in enumerate(recommendations[:3], 1):  # Show first 3
                print(f"  {i}. {product['name']}")
                print(f"     Harga: Rp {product['price']:,}")
                print(f"     Rating: {product.get('rating', 'N/A')} ({product.get('review_count', 0)} reviews)")
        else:
            print("  Tidak ada rekomendasi yang ditemukan")