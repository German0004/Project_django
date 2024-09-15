from django.contrib import admin
from .models import Picture, Reaction, Tag, Category, Comment, Article


class PictureInline(admin.TabularInline):
    model = Picture


# class LogoInline(admin.TabularInline):
#     model = Picture
#     extra = 1
#
#     class Meta:
#         verbose_name = "Logo"
#

class ArticleAdmin(admin.ModelAdmin):
    inlines = [PictureInline]


#
#
# class CategoryAdmin(admin.ModelAdmin):
#     # inlines = [LogoInline]
#     pass

admin.site.register(Picture)
admin.site.register(Reaction)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)

