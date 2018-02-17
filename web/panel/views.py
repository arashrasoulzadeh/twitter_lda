# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import TruncMonth

# Create your views here.
from models import TwitterUsers
from django.core.paginator import Paginator

from models import TwitterPost


def detail(request, id):
    user = TwitterUsers.objects.get(id=id)
    items = TwitterPost.objects.all().filter(user=user)
    rtCount = 0
    for item in items:
        if "RT" in item.text:
            rtCount += 1
    data = {
        "items": items,
        "rtCount": rtCount
    }
    return render(request, "detail.html", data)


def reports(request):
    totalRt = TwitterPost.objects.filter(text__contains="RT").count()
    totalFav = TwitterPost.objects.filter(text__contains="FAV").count()

    rtChart = TwitterPost.objects.filter(text__contains="RT").annotate(dates=TruncMonth('date')).values(
        'date').annotate(c=Count('id')).values('date', 'c')
    favsChart = TwitterPost.objects.filter(text__contains="FAV").annotate(dates=TruncMonth('date')).values(
        'date').annotate(c=Count('id')).values('date', 'c')

    data = {
        "totalRt": totalRt,
        "totalFav": totalFav,
        "favsChart": favsChart,
        "rtChart": rtChart
    }
    return render(request, "reports.html", data)


def index(request):
    users = TwitterUsers.objects.all()
    users = Paginator(users, 50)
    users = users.page(1)
    counts = []
    for user in users:
        counts = TwitterPost.objects.all().filter(user=user).count()
        user.twitts = counts

    data = {
        "users": users,
        "counts": counts
    }
    return render(request, "index.html", data)
