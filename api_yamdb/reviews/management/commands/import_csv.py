import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Импорт данных из CSV-файлов в базу данных'

    def handle(self, *args, **options):
        data_path = os.path.join(settings.BASE_DIR, 'static', 'data')

        with transaction.atomic():
            self.import_users(data_path)
            self.import_categories(data_path)
            self.import_genres(data_path)
            self.import_titles(data_path)
            self.import_genre_title(data_path)
            self.import_reviews(data_path)
            self.import_comments(data_path)

        self.stdout.write(self.style.SUCCESS('Импорт завершён.'))

    def import_users(self, data_path):
        file_path = os.path.join(data_path, 'users.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row['role'],
                        'bio': row.get('bio', ''),
                        'first_name': row.get('first_name', ''),
                        'last_name': row.get('last_name', ''),
                    },
                )
        self.stdout.write(self.style.SUCCESS('Users загружены.'))

    def import_categories(self, data_path):
        file_path = os.path.join(data_path, 'category.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    },
                )
        self.stdout.write(self.style.SUCCESS('Categories загружены.'))

    def import_genres(self, data_path):
        file_path = os.path.join(data_path, 'genre.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'slug': row['slug'],
                    },
                )
        self.stdout.write(self.style.SUCCESS('Genres загружены.'))

    def import_titles(self, data_path):
        file_path = os.path.join(data_path, 'titles.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': int(row['year']),
                        'category_id': row['category'],
                    },
                )
        self.stdout.write(self.style.SUCCESS('Titles загружены.'))

    def import_genre_title(self, data_path):
        file_path = os.path.join(data_path, 'genre_title.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        self.stdout.write(self.style.SUCCESS('Genre-Title связи загружены.'))

    def import_reviews(self, data_path):
        file_path = os.path.join(data_path, 'review.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'title_id': row['title_id'],
                        'text': row['text'],
                        'author_id': row['author'],
                        'score': int(row['score']),
                        'pub_date': row['pub_date'],
                    },
                )
        self.stdout.write(self.style.SUCCESS('Reviews загружены.'))

    def import_comments(self, data_path):
        file_path = os.path.join(data_path, 'comments.csv')
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Comment.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'review_id': row['review_id'],
                        'text': row['text'],
                        'author_id': row['author'],
                        'pub_date': row['pub_date'],
                    },
                )
        self.stdout.write(self.style.SUCCESS('Comments загружены.'))
