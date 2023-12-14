import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import MyUserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255, unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    roles = models.ManyToManyField(
        'Role', through='UserRole',
        verbose_name=('roles'))

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    @property
    def is_staff(self):
        return True

    def __str__(self):
        return f'{self.email} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'user'
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def __str__(self):
        return self.email


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(
        User, through='UserRole',
        verbose_name=('roles'))

    class Meta:
        db_table = 'role'
        verbose_name = ('Role')
        verbose_name_plural = ('Roles')

    def __str__(self):
        return self.name


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_role'
        verbose_name = ('UserRole')
        verbose_name_plural = ('UserRoles')

    def __str__(self):
        return f'{self.user.email}-{self.role.name}'
