from rest_framework import serializers
from .models import Movie, Genre, Actors, Categories, ReviewsFilm, Cinemas


class CinemasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinemas
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    # Вывод списка всех видео-объектов
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'category', 'genre', 'country')
    # year = serializers.IntegerField(default=2023)
    # title = serializers.CharField()
    # category_id = serializers.IntegerField()
    # # genre = serializers.ListField(child)
    # description = serializers.CharField()
    # country = serializers.CharField()
    # # actors = serializers.ListField()
    # image = serializers.ImageField()
    # url = serializers.URLField()


class MovieDetailSerializer(serializers.ModelSerializer):
    # Вывод полной информации о фильме по ключу(movielist/id)

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    # movie = serializers.SlugRelatedField(slug_field='title')
    # Получение отзывов
    class Meta:
        model = ReviewsFilm
        fields = "__all__"


class CinemasCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinemas
        fields = "__all__"
