from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.db.models import Avg

from .models import TestTable   

def index(request):
    template = loader.get_template('polls/index.html')

    rows = TestTable.objects.filter(venueid='El Club - Detroit, MI').values_list('date').annotate(Avg('price'))

    dic = {}
    for row in rows:
        dic[row[0]] = row[1]

    context = {
        'labels': list(dic.keys()),
        'data': list(dic.values())
    }

    return render(request, 'polls/index.html', context)