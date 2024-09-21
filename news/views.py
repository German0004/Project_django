from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from news.models import Article


def index(request: HttpRequest) -> HttpResponse:
    news = Article.objects.filter(category__name='News').order_by("created_at")[:10]
    blogs = Article.objects.filter(category__name='Blogs').count()
    interviews = Article.objects.filter(category__name='Interviews').count()
    howtodo = Article.objects.filter(category__name='HowTodo').count()
    contex = {
        'news': news,
        'blogs': blogs,
        'interviews': interviews,
        'howtodo': howtodo
    }
    return HttpResponse("<h1>Hello, world and groop 1604. You're at the new index.</h1>")
