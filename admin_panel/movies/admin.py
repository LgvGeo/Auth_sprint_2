from django.contrib import admin

from movies import models


class GenreFilmworkInline(admin.TabularInline):
    model = models.GenreFilmwork
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = models.PersonFilmwork
    autocomplete_fields = ('person',)


@admin.register(models.Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        'title', 'type',
        'creation_date', 'rating',
        'created', 'modified', 'get_genres'
    )
    list_filter = ('type', 'genres', 'persons')
    search_fields = ('title', 'description', 'id')

    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
                    super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'description')


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified')
    search_fields = ('full_name',)
