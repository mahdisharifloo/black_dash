# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import requests
import json 
from django.conf import settings



def get_statistic_data():
    url =  f"http://{settings.STATISTIC_API_URL}:10015/get_statistics"

    payload = {}
    headers = {
    'accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    resp = json.loads(response.text)
    context = {
        "label_chart11" : resp["label_chart11"] ,
        "data_chart11" : resp["data_chart11"] ,
        "label_chart12" : resp["label_chart12"] ,
        "data_chart12" : resp["data_chart12"] ,
        "label_chart13" : resp["label_chart13"] ,
        "data_chart13" : resp["data_chart13"] ,
        "label_chart2" : resp["label_chart2"] ,
        "data_chart2" : resp["data_chart2"] ,
        "label_chart3" : resp["label_chart3"] ,
        "data_chart3" : resp["data_chart3"] ,
        "label_chart4" : resp["label_chart4"] ,
        "data_chart4" : resp["data_chart4"] ,
    }
    return context

def get_news(count):
    url = f"http://{settings.STATISTIC_API_URL}:10015/get_news"

    querystring = {"record_count":f"{count}"}

    payload = ""
    headers = {"accept": "application/json"}

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    data = json.loads(response.text)
    return data


@login_required(login_url="/login/")
def index(request):
    context = get_statistic_data()
    news_list = get_news(20)
    context['rank_news_list1'] = news_list[:10]
    context['rank_news_list2'] = news_list[10:]
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    news_list = get_news(100)
    context = {'news_list1':news_list[:50],
                'news_list2':news_list[50:],
               }
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # try:

    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))
