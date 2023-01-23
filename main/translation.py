from modeltranslation.translator import register, TranslationOptions

from .models import Cinemas, Categories, Genre, Actors, Movie, ReviewsFilm


@register(Cinemas)
class CinemasTranslation(TranslationOptions):
    fields = ('name', 'description', 'address')


@register(Categories)
class CategoriesTranslation(TranslationOptions):
    fields = ('name', 'description')

@register(Genre)
class GenreTranslation(TranslationOptions):
    fields = ('name', 'description')


@register(Actors)
class ActorsTranslation(TranslationOptions):
    fields = ('name',)


@register(Movie)
class MovieTranslation(TranslationOptions):
    fields = ('title', 'country', 'description', )


