from django.contrib import admin
from .models import Picture, Reaction, Tag, Category, Comment, Article

admin.site.register(Picture)
admin.site.register(Reaction)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Article)
