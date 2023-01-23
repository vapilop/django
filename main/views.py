from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .forms import ReviewForm
from .models import Movie, Genre, ReviewsFilm, Cinemas
from .serializers import MovieSerializer, MovieDetailSerializer, ReviewCreateSerializer, CinemasSerializer, \
    CinemasCreateSerializer

from .service import MovieFilter

import csv

from simple_history.models import HistoricalRecords

def export_to_csv(request):
    movies = Movie.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=movies_export.csv; encoding="cp1251"; newline="";'
    writer = csv.writer(response)
    writer.writerow(['Год', 'Название', 'Описание', 'Страна', 'Изображение' 'Ссылка'])
    movies_fields = movies.values_list('year', 'title', 'description', 'country',
                                      'image', 'url')
    for movie in movies_fields:
        writer.writerow(movie)
    return response


class MoscinoSaturn(ListView):
    model = Cinemas
    queryset = Cinemas.objects.filter(url='moscino-saturn')
    template_name = 'movies/moscino-saturn.html'


class GenreYears:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        years_sorted_list = sorted(set(Movie.objects.values_list('year', flat=True)))
        return years_sorted_list


class MoviesView(GenreYears, ListView):
    # Список фильмов
    model = Movie
    queryset = Movie.objects.all()
    paginate_by = 3
    ordering = ['-id']
    template_name = 'movies/movie_list.html'


class AnimationView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(category_id=2)
    paginate_by = 6
    ordering = ['-id']
    template_name = 'movies/animation_list.html'


class OnlyMoviesView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(category_id=1)
    paginate_by = 6
    ordering = ['-id']
    template_name = 'movies/onlymovies_list.html'
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Categories.objects.all()
    #     return context


class ComedyGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='comedy')
    paginate_by = 6
    template_name = 'movies/comedy_list.html'


class HorrorGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='horror')
    paginate_by = 6
    template_name = 'movies/horror_list.html'


class CartoonGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='cartoon')
    paginate_by = 6
    template_name = 'movies/cartoon_list.html'


class ActionFilmGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='action_film')
    paginate_by = 6
    template_name = 'movies/action_film_list.html'


class FantasticGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='fantastic')
    paginate_by = 6
    template_name = 'movies/fantastic_list.html'


class TrillerGenreView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(genre__url='triller')
    paginate_by = 6
    template_name = 'movies/triller_list.html'


class MovieDetailView(GenreYears, DetailView):
    # Карточка фильма
    model = Movie
    slug_field = "url"
    template_name = 'movies/movie_detail.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Categories.objects.all()
    #     return context


class AddReview(View):
    # Добавление отзыва
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class SearchBar(ListView):
    template_name = 'movies/movie_list.html'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q').capitalize()
        return Movie.objects.filter(title__icontains=q)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


# Апипишка

class CinemasAPIView(generics.ListAPIView):
    # Вывод списка кинотеатров
    serializer_class = CinemasSerializer

    def get_queryset(self):
        cinemas = Cinemas.objects.all()
        return cinemas


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.all()
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer



# class MoviesAPIView(generics.ListAPIView):
#     # Вывод кино и мультфильмов
#     serializer_class = MovieSerializer
#
#     def get_queryset(self):
#         movies = Movie.objects.all()
#         return movies
#

class MoviesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # Вывод полной информации по конкретному фильму/мультику
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


class ReviewsCreateFilmAPIView(generics.CreateAPIView):
    # получение и создание отзыва
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = ReviewsFilm.objects.all()
        return Response({'reviews': ReviewCreateSerializer(queryset, many=True).data})

    serializer_class = ReviewCreateSerializer


class CinemasCreateAPIView(generics.CreateAPIView):
    # Получение и создание киноетатра
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = Cinemas.objects.all()
        return Response({'cinemas': CinemasCreateSerializer(queryset, many=True).data})

    serializer_class = CinemasCreateSerializer
