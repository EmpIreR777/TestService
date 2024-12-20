from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользовательский интерфейс в админке для модели User."""

    list_display = (
        'email', 'first_name',
        'last_name', 'username',
        'is_staff', 'is_active',
    )
    list_filter = (
        'is_staff', 'is_active',
    )
    search_fields = (
        'email', 'first_name',
        'last_name', 'username',
    )
    ordering = ('email',)
