import simple_history
from django.contrib import admin
from django import forms
from simple_history.admin import SimpleHistoryAdmin

from .models import Actors, Categories, Cinemas, Genre, Movie, ReviewsFilm
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from modeltranslation.admin import TranslationAdmin

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Description', widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


admin.site.site_title = 'КиноАфиша'
admin.site.site_header = 'КиноАфиша'


@admin.register(Actors)
class ActorsAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'age', 'get_image')
    readonly_fields = ('get_image',)
    list_display_links = ('name',)
    ordering = ('id',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Categories)
class CategoriesAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)
    ordering = ('id',)


@admin.register(Cinemas)
class CinemasAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'description', 'number', 'address', 'url')
    list_display_links = ('name', 'number')
    ordering = ('id',)


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)
    ordering = ('id',)


class ReviewsInFilms(admin.TabularInline):
    model = ReviewsFilm
    extra = 0
    readonly_fields = ('name', 'email')


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'category', 'get_image', 'url')
    list_filter = ('category', 'year', 'genre',)
    search_fields = ('title', 'category__name',)
    readonly_fields = ('get_image',)
    list_display_links = ('title',)
    raw_id_fields = ['genre', 'category']
    inlines = [ReviewsInFilms]
    save_on_top = True
    save_as = True
    search_help_text = False
    ordering = ('id',)
    #form = MovieAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'

#
# @admin.register(RatingFilm)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = ('id', 'movie', 'value')
#     list_display_links = ('movie',)
#     ordering = ('id',)


@admin.register(ReviewsFilm)
class ReviewsFilmAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('id', 'movie', 'email', 'text')
    readonly_fields = ('name', 'email', 'movie')
    list_display_links = ('movie',)
    ordering = ('id',)
