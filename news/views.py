from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Hello, world. You're at the new index.</h1>")
