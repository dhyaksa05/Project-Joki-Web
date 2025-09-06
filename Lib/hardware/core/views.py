from django.shortcuts import render
from django.http import HttpResponse
from .models import Produk  # ✅ bukan Hardware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def home(request):
    return render(request, 'index.html')

def processor(request):
    return render(request, 'processor.html')

def rekomendasi_view(request):
    results = []
    budget = ''
    usage = ''
    custom_usage = ''
    komponen = []

    if request.method == 'POST':
        budget = request.POST.get('budget')
        usage = request.POST.get('usage')
        custom_usage = request.POST.get('custom_usage', '')
        komponen = request.POST.getlist('components')

        query_text = (usage or '') + " " + custom_usage

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

    context = {
        'results': results,
        'budget': budget,
        'usage': usage,
        'custom_usage': custom_usage,
        'komponen': komponen,
    }
    return render(request, 'hasil.html', context)
