from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Movie


class MovieFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = ['genre', 'title']
