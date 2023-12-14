from rest_framework import serializers

from movies.models import Filmwork, Genre, Person


class GenreForMovieSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.name

    class Meta:
        model = Genre
        fields = ('name',)


class PersonForMovieSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return instance.full_name

    class Meta:
        model = Person
        fields = ('full_name',)


class MovieSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        serialized_obj = super().to_representation(instance)
        actors = instance.actors
        directors = instance.directors
        writers = instance.writers
        genres = instance.genres
        serialized_obj['genres'] = GenreForMovieSerializer(
            genres, many=True).data
        serialized_obj['actors'] = PersonForMovieSerializer(
            actors, many=True).data
        serialized_obj['directors'] = PersonForMovieSerializer(
            directors, many=True).data
        serialized_obj['writers'] = PersonForMovieSerializer(
            writers, many=True).data
        return serialized_obj

    class Meta:
        model = Filmwork
        fields = (
            'id', 'title',
            'description', 'creation_date',
            'rating', 'type')
