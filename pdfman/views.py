from django.shortcuts import render
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
OUTPUT_PATH = f'{Path(__file__).resolve().parent.parent}/media/pdf/'

def pdfman(request):
    return render(request, 'pdfman/pdf.html')