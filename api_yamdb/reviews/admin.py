from django.contrib import admin

from .models import Category, Genre, Title

class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category', 'genre')
    search_fields = ('category', 'genre',)
    list_filter = ('name', 'category', 'genre', 'year',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)