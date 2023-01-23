from django import template

from main.models import Categories, Movie, Genre, Cinemas

register = template.Library()


@register.simple_tag()
# Вывод категорий на сайте
def get_categories():
    return Categories.objects.all()

@register.simple_tag()
def get_genres():
    return Genre.objects.all()

@register.simple_tag()
def get_cinemas():
    return Cinemas.objects.all()

@register.simple_tag()
def get_moscino():
    return Cinemas.objects.filter(url='moscino-saturn').get()

@register.simple_tag()
def get_years():
    years_sorted_list = sorted(set(Movie.objects.values_list('year', flat=True)))
    return years_sorted_list


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies():
    movies = Movie.objects.order_by('-id')[:5]
    return {'last_movies': movies}
