# Generated by Django 5.1.1 on 2024-09-21 12:09

import django.db.models.deletion
import news.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(unique=True, upload_to=news.models.get_image_path)),
                ('description', models.TextField(blank=True, default='no description provided')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('description', models.TextField(blank=True, default='no description provided')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.category')),
                ('logo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.picture')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='news.tag')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='news.category')),
                ('main_picture', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='for_article', to='news.picture')),
                ('pictures', models.ManyToManyField(blank=True, related_name='articles', to='news.picture')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.article')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.comment')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emojy', models.CharField(choices=[('😀', 'Grinning Face'), ('😁', 'Grinning Face With Smiling Eyes'), ('😂', 'Face With Tears Of Joy'), ('🥰', 'Smiling Face With Hearts'), ('🤩', 'Star Struck'), ('🤮', 'Face Vomiting'), ('😈', 'Smiling Face With Horns'), ('👿', 'Angry Face With Horns'), ('😡', 'Angry Face'), ('💩', 'Pile Of Poo'), ('❤', 'Red Heart'), ('👍', 'Thumbs Up'), ('👎', 'Thumbs Down'), ('👏', 'Clapping Hands'), ('🤝', 'Handshake'), ('🇺🇦', 'Ukraine')], max_length=3)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='reactions',
            field=models.ManyToManyField(blank=True, related_name='articles', to='news.reaction'),
        ),
    ]
