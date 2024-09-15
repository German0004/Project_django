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
    logo  = OneToOneField(Picture, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name