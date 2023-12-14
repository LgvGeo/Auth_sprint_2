# Generated by Django 3.2 on 2023-12-10 15:20

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_role',
            },
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(through='users.UserRole', to=settings.AUTH_USER_MODEL, verbose_name='roles'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(through='users.UserRole', to='users.Role', verbose_name='roles'),
        ),
    ]
