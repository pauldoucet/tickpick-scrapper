from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.db.models import Avg, Max, Min

from .models import TestTable   

def index(request):
    template = loader.get_template('polls/index.html')

    venue_tuples = TestTable.objects.values_list('venueid').distinct()

    venue_list = []
    for venue in venue_tuples:
        venue_list.append(venue[0])

    rows = TestTable.objects.filter(venueid='El Club - Detroit, MI').values_list('date').annotate(Avg('price'))

    dic = {}
    for row in rows:
        dic[row[0]] = row[1]

    context = {
        'venue_list': list(venue_list),
        'labels': list(dic.keys()),
        'data': list(dic.values()),
    }

    return render(request, 'polls/index.html', context)


def venue_data(request, venue_index):
    template = loader.get_template('polls/index.html')

    venue_tuples = TestTable.objects.values_list('venueid').distinct()

    venue_list = []
    for venue in venue_tuples:
        venue_list.append(venue[0])
   
    venueid = venue_list[venue_index]

    rows = TestTable.objects.filter(venueid=venueid).values_list('date').annotate(Avg('price'), Min('price'), Max('price'))

    dic_average = {}
    dic_max = {}
    dic_min = {}
    for row in rows:
        dic_max[row[0]] = row[3]
        dic_min[row[0]] = row[2]
        dic_average[row[0]] = row[1]

    return JsonResponse(data={
        'labels': list(dic_average.keys()),
        'average': list(dic_average.values()),
        'maximum': list(dic_max.values()),
        'minimum': list(dic_min.values()),
        'label': venueid,
    })