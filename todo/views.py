from django.shortcuts import render
from rest_framework import viewsets          # add this
from .serializers import TodoSerializer      # add this
from .models import Todo                     # add this
import requests


def loadData():
    baseUrl = 'https://hacker-news.firebaseio.com/v0/item/'
    hnIdList = []
    hackerStory = []
    response = requests.get(
        'https://hacker-news.firebaseio.com/v0/topstories.json/')
    hackerData = response.json()
    for x in range(0, 10):
        hnIdList.append(hackerData[x])
    while hnIdList:
        storyId = hnIdList.pop()
        responseId = requests.get(
            baseUrl + str(storyId) + '.json'
        )
        hackerStory.append(responseId.json())
    for data in hackerStory:
        by = data['by'],
        title = data['title'],
        url = data['url'],
        score = data['score']
        todo, created = Todo.objects.get_or_create(
            by=by,
            title=title,
            url=url,
            score=score
        )
        if created:
            todo.save()


class TodoView(viewsets.ModelViewSet):       # add this
    serializer_class = TodoSerializer          # add this
    loadData()
    queryset = Todo.objects.all()              # add this
