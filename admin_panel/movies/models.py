import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypeChoices(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), null=True)
    genres = models.ManyToManyField(
        Genre, through='GenreFilmwork',
        verbose_name=_('genres'))
    persons = models.ManyToManyField(
        Person, through='PersonFilmwork', verbose_name=_('persons'))
    rating = models.FloatField(
        _('rating'),
        validators=[MaxValueValidator(100), MinValueValidator(0)])
    type = models.CharField(
        _('type'), choices=TypeChoices.choices, max_length=32)

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('GenreFilmwork')
        verbose_name_plural = _('GenreFilmworks')
        indexes = (
            models.Index(fields=('genre', 'film_work')),
        )
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'film_work'),
                name='unique_genre_film_work'),
        )
    
    def __str__(self):
        return f'{self.film_work.title}-{self.genre.name}'


class PersonFilmwork(UUIDMixin):

    class RoleChoices(models.TextChoices):
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE
    )
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        _('role'),
        choices=RoleChoices.choices, max_length=255
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('PersonFilmwork')
        verbose_name_plural = _('PersonFilmworks')
        indexes = (
            models.Index(fields=('film_work', 'person')),
        )

    def __str__(self):
        return f'{self.film_work.title}-{self.person.full_name}'
