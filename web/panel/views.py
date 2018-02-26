# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.core.cache import cache
# Create your views here.
from django.urls import reverse
from panel.models import *
from django.core.paginator import Paginator
import re


def getUserId(username):
    user = TwitterUsers.objects.all().filter(username=username)
    if len(user) is 0:
        return username
    user = user.first()
    return user.id


def tweet(request, id):
    import nltk
    from senti_classifier import senti_classifier
    t = TwitterPost.objects.all().filter(id=id).first()
    sentence = t.text
    tokens = nltk.word_tokenize(sentence)
    pos_score, neg_score = senti_classifier.polarity_scores([t.text])
    tagged = nltk.pos_tag(tokens)
    import os
    from nltk.tree import Tree
    from nltk.draw.tree import TreeView
    tr = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')
    TreeView(tr)._cframe.print_to_file('output.ps')
    os.system('convert output.ps output.png')
    os.system('cp output.png static/tree.png')
    entities = nltk.chunk.ne_chunk(tagged)

    data = {"twitt": t,
            "tokens": tokens,
            "tags": entities,
            "pos_score": pos_score,
            "neg_score": neg_score}
    return render(request, "tweet.html", data)


def hashtags(request, hashtag):
    tags = TwitterPost.objects.all().filter(text__contains="#" + hashtag)
    for item in tags:
        item.text = makeHtml(item.text)

    data = {
        "items": tags
    }

    return render(request, "hashtags.html", data)


def makeHtml(text):
    mentions = re.findall(r"@(\w+)", text)
    for mention in mentions:
        text = text.replace("@" + mention, "<a href='/?q=" + getUserId(mention) + "'>@" + mention + "</a>")
    hashtags = re.findall(r"#(\w+)", text)
    for hashtag in hashtags:
        url = reverse('hashtags', kwargs={'hashtag': hashtag})
        text = text.replace("#" + hashtag, "<a href='" + url + "'>#" + hashtag + "</a>")
    return text


def getUserRemoteID(user):
    import requests

    url = "https://tweeterid.com/ajax.php"
    response = requests.post(url, data={"input": user})
    print(user, response.text)
    return str(response.text)


def bulkuser(request):
    userandid = []
    if request.POST.get("users"):
        users = request.POST.get("users").split(",")
        for user in users:
            userandid += [{
                "user": user,
                "id": getUserRemoteID(user)
            }]

    data = {
        "items": userandid
    }
    return render(request, "bulk.html", data)


def detail(request, id):
    user = TwitterUsers.objects.get(id=id)
    items = TwitterPost.objects.all().filter(user=user)
    user_id = getUserRemoteID(user.username[12:])
    twitts = []
    for item in items:
        item.text = makeHtml(item.text)
        text = item.text
        twitts += [{
            "id": item.id,
            "text": text,
            "date": item.date,

        }]
    rtCount = 0
    mentionCount = 0
    for item in items:
        if "RT" in item.text:
            rtCount += 1
    for item in items:
        if "@" in item.text:
            mentionCount += 1

    data = {
        "items": twitts,
        "userid": user_id,
        "rtCount": rtCount,
        "mentionCount": mentionCount
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


def getUserTwittsCount(user):
    key = str(user.id) + "_twitts_count"
    if cache.has_key(key):
        print("returing cache")
        return cache.get(key)
    else:
        print("creating cache")
        counts = TwitterPost.objects.all().filter(user=user).count()
        cache.set(key, counts, timeout=22)
        cache.persist(key)
        return counts


def index(request):
    users = TwitterUsers.objects.all()
    if request.GET.get("q"):
        query = request.GET.get("q")
        users = TwitterUsers.objects.all().filter(username__contains=query)

    counts = []

    for user in users:
        user.twitts = getUserTwittsCount(user)

    # users = sorted(users, key=lambda twitts: users.twitts)  # sort by age
    users = Paginator(users, 50)
    users = users.page(1)

    data = {
        "users": users,
        "counts": counts
    }
    return render(request, "index.html", data)
