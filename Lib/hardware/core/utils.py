import re
import string

def text_preprocessing(text):
    """
    Fungsi untuk membersihkan dan menormalisasi teks sebelum masuk TF-IDF.
    """
    if not text:
        return ""

    # 1. Case Folding (Ubah ke huruf kecil)
    text = text.lower()

    # 2. Cleaning (Hapus URL, angka, tanda baca)
    text = re.sub(r'http\S+|www\.\S+', '', text) # Hapus URL
    text = re.sub(r'\d+', '', text) # Hapus angka (opsional, tapi biasanya spek angka penting. Kalo mau hapus, uncomment baris ini)
    text = text.translate(str.maketrans('', '', string.punctuation)) # Hapus tanda baca

    # 3. Normalisasi Istilah Hardware (PENTING BUAT SKRIPSI/TUGAS)
    # Ini biar dosen liat lu ngerti domain knowledge-nya
    replacements = {
        'proc': 'processor',
        'cpu': 'processor',
        'mobo': 'motherboard',
        'mainboard': 'motherboard',
        'vga': 'gpu',
        'graphic card': 'gpu',
        'graphics card': 'gpu',
        'ram': 'memory',
        'ssd': 'storage',
        'hdd': 'storage',
        'psu': 'power supply',
        'spek': 'spesifikasi',
        'murah': '', # Hapus kata marketing spam
        'terbaik': '',
        'promo': '',
        'diskon': ''
    }
    
    for slang, formal in replacements.items():
        text = re.sub(r'\b' + slang + r'\b', formal, text)

    # 4. Hapus whitespace berlebih
    text = " ".join(text.split())

    return text