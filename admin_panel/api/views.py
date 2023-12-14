from django.db.models import Prefetch
from rest_framework import viewsets

from api.paginators import MoviePagination
from api.serializers import MovieSerializer
from movies.models import Filmwork, Person


class MovieReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = MoviePagination
    serializer_class = MovieSerializer
    queryset = Filmwork.objects.prefetch_related(
        'genres',
        Prefetch(
            'persons',
            queryset=Person.objects.filter(
                personfilmwork__role='actor').distinct(),
            to_attr='actors'
        ),
        Prefetch(
            'persons',
            queryset=Person.objects.filter(
                personfilmwork__role='director').distinct(),
            to_attr='directors'
        ),
        Prefetch(
            'persons',
            queryset=Person.objects.filter(
                personfilmwork__role='writer').distinct(),
            to_attr='writers'
        )
    )
