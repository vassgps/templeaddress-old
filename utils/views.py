#webapp/utils/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'utils/index.html')

def about(request):
    return render(request, 'utils/about.html')
