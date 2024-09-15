from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello, world and groop 1604. You're at the new index.</h1>")
