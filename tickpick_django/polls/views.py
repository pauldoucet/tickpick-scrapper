from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.db.models import Avg

from .models import TestTable

def pie(request):
    template = loader.get_template('polls/pie.html')

    rows = TestTable.objects.filter(venueid='Warsaw - Brooklyn, NY').values_list('date').annotate(Avg('price'))

    dic = {}
    for row in rows:
        dic[row[0]] = row[1]

    context = {
        'labels': list(dic.keys()),
        'data': list(dic.values())
    }

    return render(request, 'polls/pie.html', context)    

def index(request):
    template = loader.get_template('polls/index.html')

    rows = TestTable.objects.filter(venueid='Warsaw - Brooklyn, NY').values_list('date').annotate(Avg('price'))

    dic = {}
    for row in rows:
        dic[row[0]] = row[1]

    context = {
        'labels': list(dic.keys()),
        'data': list(dic.values())
    }

    return render(request, 'polls/index.html', context)

# def diagram(request):
#     dates = TestTable.objects.values_list('date', flat = True).distinct()
#     backgroundColor = '#79AEC8'
#     borderColor = '#417690'
#     rows = TestTable.objects.filter(venueid='Warsaw - Brooklyn, NY').values_list('date').annotate(Avg('price'))

#     dic = {}
#     for row in rows:
#         dic[row[0]] = row[1]

#     return JsonResponse({
#         'type': 'bar',
#         'data': {
#             'labels': list(dic.keys()),
#             'datasets': [
#                 {
#                     'label': 'Price ($)',
#                     'backgroundColor': backgroundColor,
#                     'borderColor': borderColor,
#                     'data': list(dic.values())
#                 }
#             ]

#         },
#         'options': {
#             'title': {
#                 'text': "Price evolution",
#                 'display': True
#             }
#         }
#     })



def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)