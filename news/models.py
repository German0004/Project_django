from functools import reduce
from pathlib import Path
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.TextField(blank=True, default="no description provided")

    def __str__(self):
        return self.name

    def save(
            self,
            *args,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        name = reduce(lambda acc, x: acc + x if x.isalpha() else ' ', tuple(self.name))
        name = "".join(
            map(str.capitalize, name.split())
        )
        self.name = "#" + name
        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Reaction(models.Model):
    class PossibleReactions(models.TextChoices):
        GRINNING_FACE = "😀"
        GRINNING_FACE_WITH_SMILING_EYES = "😁"
        FACE_WITH_TEARS_OF_JOY = "😂"
        SMILING_FACE_WITH_HEARTS = "🥰"
        STAR_STRUCK = "🤩"
        FACE_VOMITING = "🤮"
        SMILING_FACE_WITH_HORNS = "😈"
        ANGRY_FACE_WITH_HORNS = "👿"
        ANGRY_FACE = "😡"
        PILE_OF_POO = "💩"
        RED_HEART = "❤"
        THUMBS_UP = "👍"
        THUMBS_DOWN = "👎"
        CLAPPING_HANDS = "👏"
        HANDSHAKE = "🤝"
        UKRAINE = "🇺🇦"

    emojy = models.CharField(max_length=3, choices=PossibleReactions)
    article = models.ForeignKey("news.Article", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.emojy


def get_image_path(instance, filename=str, subfolder: Path = Path("pictures/")) -> Path:
    filename = (
            f"{slugify(filename.partition('.')[0])}_{uuid4()}" + Path(filename).suffix
    )
    return Path(subfolder) / filename


class Picture(models.Model):
    image = models.ImageField(upload_to=get_image_path, unique=True)
    description = models.TextField(blank=True, default="no description provided")

    def __str__(self):
        return self.image.name


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(blank=True, default="no description provided")
    logo = models.OneToOneField(Picture, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    pictures = models.ManyToManyField(Picture, blank=True, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True)
    reactions = models.ManyToManyField(Reaction, blank=True, related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_picture = models.OneToOneField(Picture, on_delete=models.SET_NULL, null=True, related_name="for_article_main")

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.RESTRICT)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.text}"
