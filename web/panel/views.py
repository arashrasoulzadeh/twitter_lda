# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

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
    return render(request, "reports.html")


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
