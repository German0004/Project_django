import pathlib
import random

from typing import Sequence, Optional, Dict

from django.core.files.images import ImageFile
from django.db import IntegrityError, transaction
from django.db.models import QuerySet

import django_init
from news.models import Tag, Reaction, Picture, Article, Comment, Category
from django.contrib.auth import get_user_model
from faker import Faker

#  логіка роботи можливостей розміщати матеріали:
# (у вбудованій системі автентифікації-авторизації) одразу у User є поля булевські поля is_staff, is_superuser
# звісно ми можемо створити ще якісь свої кастомні для додаткової класифікації користувачів - але не зараз
# для учбового проекту цього буде достатньо
# всі статті обовʼязково мають категорії, ми їх зробимо 4
# - News (новини)
# - Interview (інтервʼю)
# - HowToDo (як зробити)
# - Blog (блог)
#
# легенда така:
# - автори новин і інтервʼю - новини і інтервʼю можуть постити лише суперкористувачі (редакційна політика) -
# is_superuser
# - автори статей HowTo - HowToDo (як зробити) - постять запрошувані фахівці, які не є співробітниками,
# але їх саме для цього запрсила редакція, вони мають статус is_staf
# - автори блогів - Blog (блог) - може створити і додати матеріал будь-який зареєстрований користувач
# - автори коментів, реакцій - коментувати будь-що може будь-який зареєстрований користувач

User = get_user_model()

faker = Faker(["uk_UA", "en_US"])


def create_fake_superuser(num: int = 3, fake_generator: Faker = faker) -> list[int | str]:
    user_created = []
    for _ in range(num):
        try:
            user = User.objects.create_superuser(
                username=fake_generator.user_name(),
                email=fake_generator.free_email(),
                password=fake_generator.password(),
                first_name=fake_generator.first_name(),
                last_name=fake_generator.last_name(),
                is_staff=True,
                is_superuser=True,
            )
            user_created.append(user.id)
        except IntegrityError as e:
            print(str(e))
            user_created.append(str(e))
    return user_created


def create_fake_user(num: int = 3, fake_generator: Faker = faker, *, is_staff: bool = False) -> list[int | str]:
    user_created = []
    for _ in range(num):
        try:
            user = User.objects.create_user(
                username=fake_generator.user_name(),
                email=fake_generator.free_email(),
                password=fake_generator.password(),
                first_name=fake_generator.first_name(),
                last_name=fake_generator.last_name(),
                is_staff=is_staff,
            )
            user_created.append(user.id)
        except IntegrityError as e:
            print(str(e))
            user_created.append(str(e))
    return user_created


def create_fake_category(
        name: str,
        image_path: pathlib.Path,
        description: str = "no description provided"
) -> int | str:
    if not image_path.is_file():
        return f"File {image_path} not found"

    try:
        with transaction.atomic():
            with open(image_path, "rb") as f:
                category_logo = Picture.objects.create(
                    image=ImageFile(f),
                    description=f"Logo for category {name}"
                )
            category = Category.objects.create(
                name=name,
                description=description,
                logo=category_logo
            )
        return category.id
    except IntegrityError as e:
        return str(e)


def create_face_tags(num: int = 10, fake_generator: Faker = None, max_word_in_tag: int = 3) -> list[int | str]:
    if not fake_generator:
        fake_generator = Faker(["uk_UA"])
    num_words = [num for num in range(1, max_word_in_tag + 1)]
    tag_ids = []
    for _ in range(num):
        while True:
            # тут я генерую поки не буде менше 16 символів (обмеження БД)
            name = " ".join(fake_generator.words(nb=fake_generator.random_element(num_words)))
            if len(name) < 16:
                break
        try:
            tag = Tag.objects.create(
                name=name,
                description=fake_generator.text()
            )
            tag_ids.append(tag.id)
        except IntegrityError as e:
            print(str(e))
            tag_ids.append(str(e))
    return tag_ids


def create_fake_article(
        title: str,
        text: str,
        posted_by: User,
        category: Category,
        main_picture: pathlib.Path | None,
        pictures: Sequence[pathlib.Path] | None,
        tags: Sequence[Tag] | None = None,
) -> int | str:
    try:
        with transaction.atomic():
            article = Article(
                title=title,
                text=text,
                posted_by=posted_by,
                category=category,
            )
            if main_picture:
                with open(main_picture, "rb") as f:
                    main_picture = Picture.objects.create(
                        image=ImageFile(f),
                        description=f"Main picture for article {title}"
                    )
                article.main_picture = main_picture
            article.save()
            if pictures:
                set_pictures = set()
                for num, pictures_path in enumerate(pictures, start=1):
                    with open(pictures_path, "rb") as f:
                        picture = Picture.objects.create(
                            image=ImageFile(f),
                            description=f"Picture {num} for article {title}"
                        )
                    set_pictures.add(picture)
                article.pictures.set(set_pictures)
            if tags:
                article.tags.set(tags)
        return article.id
    except IntegrityError as e:
        return str(e)


def create_fake_articles(
        num: int,
        category: Category,
        text_symbols: int = 1000,
        title_words: int = 5,
        posted_by_set: Optional[QuerySet[User]] = None,
        folder_with_pictures: pathlib.Path = pathlib.Path("image/pictures"),
        main_picture_model: Optional[list[int]] = None,
        pictures_num_model: Optional[list[int]] = None,
        tags_set: Optional[QuerySet[Tag]] = None,
        tags_num_model: Optional[list[int]] = None,
        **kwargs
) -> list[int | str]:
    if not posted_by_set:
        posted_by_set = User.objects.filter(is_superuser=True)
    if not main_picture_model:
        main_picture_model = [0, 1]
    if not tags_set:
        tags_set = Tag.objects.all()
    if not tags_num_model:
        tags_num_model = [1, 2, 2, 3, 3, 4]
    if not pictures_num_model:
        pictures_num_model = [0, 0, 0, 0, 1, 1, 2, 3]
    pictures_paths = [path for path in folder_with_pictures.glob("*.*") if path.is_file()]
    results = []
    for _ in range(num):
        results.append(
            create_fake_article(
                title=faker.sentence(nb_words=title_words),
                text=faker.text(max_nb_chars=text_symbols),
                posted_by=faker.random_element(posted_by_set),
                category=category,
                main_picture=faker.random_element(pictures_paths) if faker.random_element(main_picture_model) else None,
                pictures=faker.random_elements(elements=pictures_paths,
                                               length=faker.random_element(pictures_num_model)),
                tags=faker.random_elements(elements=tags_set,
                                           length=faker.random_element(tags_num_model)),
            )
        )
    return results


def create_fake_comment(
        article: Article,
        posted_by: User,
        parent: Comment | None = None,
) -> Comment:
    if parent:
        comment = Comment.objects.create(
            text=faker.text(max_nb_chars=random.randint(30, 500)),
            article=parent.article,
            posted_by=posted_by,
            parent=parent
        )
    comment = Comment.objects.create(
        text=faker.text(max_nb_chars=random.randint(30, 500)),
        article=article,
        posted_by=posted_by,
    )
    return comment


def create_fake_comments(
        num_without_parent: int,
        parent: bool = True,
        articles: Optional[QuerySet[Article]] = None,
        posted_by: Optional[QuerySet[User]] = None,
) -> list[int | str]:
    results = []
    if articles is None:
        articles = Article.objects.all()
    if posted_by is None:
        posted_by = User.objects.all()
    for _ in range(num_without_parent):
        try:
            with transaction.atomic():
                article = faker.random_element(articles)
                comment = create_fake_comment(
                    article=article,
                    posted_by=faker.random_element(posted_by),
                )
                results.append(comment.id)
                # parent comments - 20% of all comments if parent is True
                while parent and faker.random_element((1, 0, 0, 0, 0)):
                    comment = create_fake_comment(
                        article=comment.article,
                        posted_by=faker.random_element(posted_by),
                        parent=comment,
                    )
                    results.append(comment.id)
        except IntegrityError as e:
            print(str(e))
            results.append(str(e))
    return results


def add_fake_reactions(
        article_set: QuerySet[Article],
        user_set: QuerySet[User],
        possible_reactions: Sequence[str] = Reaction.PossibleReactions.values,
        reactions_num_model: Optional[list[int]] = None,
) -> list[int | str]:
    if not reactions_num_model:
        reactions_num_model = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    for article in article_set:
        for _ in range(faker.random_element(reactions_num_model)):
            try:
                reaction = Reaction.objects.create(
                    emojy=faker.random_element(possible_reactions),
                    article=article,
                    user=faker.random_element(set(user_set))
                )
                results.append(reaction.id)
            except IntegrityError as e:
                print(str(e))
                results.append(str(e))
    return results


if __name__ == "__main__":
    print(create_fake_superuser(3))
    print(create_fake_user(10, is_staff=True))
    print(create_fake_user(100))

    print(create_fake_category(
        "News",
        pathlib.Path("image/logo/news_logo.png"),
        "News category"
    ))
    print(create_fake_category(
        "Blogs",
        pathlib.Path("image/logo/blog_logo.png"),
        "Blogs category"
    ))
    print(create_fake_category(
        "Interviews",
        pathlib.Path("image/logo/interview_logo.png"),
        "Interviews category"
    ))
    print(create_fake_category(
        "HowToDo",
        pathlib.Path("image/logo/how_it_works_logo.png"),
        "HowToDo category"
    ))

    print(create_face_tags(30))

    # фейкові новини
    print(create_fake_articles(
        100,
        Category.objects.get(name="News"),

    ))

    # фейкові інтервʼю
    print(create_fake_articles(
        10,
        Category.objects.get(name="Interviews"),
        text_symbols=3000,
        title_words=10,
        main_picture_model=[1],
    ))

    # фейкові статті HowToDo
    print(create_fake_articles(
        10,
        category=Category.objects.get(name="HowToDo"),
        posted_by_set=User.objects.filter(is_staff=True),
        text_symbols=3000,
        title_words=10,
        main_picture_model=[1],
        pictures_num_model=[2, 3, 3, 4]
    ))

    # фейкові блоги
    print(create_fake_articles(
        100,
        Category.objects.get(name="Blogs"),
        text_symbols=2000,
        title_words=10,
        main_picture_model=[0, 1],
        posted_by_set=User.objects.filter(is_staff=False),
    ))

    # фейкові коментарі
    print(create_fake_comments(300))

    # фейкові реакції
    print(add_fake_reactions(
        Article.objects.all(),
        User.objects.filter(is_superuser=False),
    ))