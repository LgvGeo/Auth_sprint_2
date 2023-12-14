from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from passlib.hash import pbkdf2_sha512

from users.models import User, UserRole


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords doesn\'t match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = pbkdf2_sha512.hash(user.password)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'roles']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = pbkdf2_sha512.hash(user.password)
        if commit:
            user.save()
        return user


class UserRoleForm(forms.ModelForm):
    role = forms.CharField()


class UserRoleInline(admin.TabularInline):
    model = UserRole
    fields = ['role']


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (UserRoleInline,)
    list_display = [
        'email', 'first_name', 'last_name', 'created_at', 'get_roles']
    list_filter = []
    list_prefetch_related = ('roles',)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        queryset = (
                    super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_roles(self, obj):
        return ','.join([role.name for role in obj.roles.all()])

    get_roles.short_description = 'Роли'

    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ['first_name', 'last_name']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': [
                    'email', 'password',
                    'password2', 'first_name', 'last_name'
                ],
            },
        ),
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
