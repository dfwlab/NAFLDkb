from django.shortcuts import render
from models import News, Publications, Updates
# Create your views here.


def index2(request):
    result = {}
    result['news'] = News.objects.filter(new=1)
    result['publications'] = Publications.objects.filter(new=1)
    result['updates'] = Updates.objects.filter(new=1)
    return render(request, 'index.html', result)
