from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

class Cinemas(models.Model):
    # Список доступных кинотеатров
    name = models.CharField('Кинотеатр', max_length=150)
    description = models.TextField('Описание')
    number = models.PositiveSmallIntegerField('Контактный номер', help_text='Введите номер кинотеатра')
    address = models.CharField('Адрес кинотеатра', max_length=150)
    url = models.SlugField(max_length=150, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кинотеатр'
        verbose_name_plural = 'Кинотеатры'


class Categories(models.Model):
    # Список категорий
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    # Список жанров
    name = models.CharField('Жанр', max_length=100, help_text='')
    description = models.TextField('Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Actors(models.Model):
    # Актеры
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры'
        verbose_name_plural = 'Актеры'


class Movie(models.Model):
    # Список фильмов
    year = models.PositiveSmallIntegerField('Дата выхода', default=2023)
    title = models.CharField('Название', max_length=100)
    category = models.ForeignKey(Categories, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    description = models.TextField('Описание')
    country = models.CharField('Страна', max_length=30)
    actors = models.ManyToManyField(Actors, verbose_name='Актеры', related_name='film_actor')
    image = models.ImageField('Постер', upload_to='movies/')
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class RatingFilm(models.Model):
    # Рейтинг фильма
    value = models.FloatField('Рейтинг фильма', default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f"{self.value} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class ReviewsFilm(models.Model):
    # Отзывы к фильму
    email = models.EmailField()
    name = models.CharField('Имя пользователя', max_length=100)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)
    text = models.TextField('Отзыв', max_length=5000)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
