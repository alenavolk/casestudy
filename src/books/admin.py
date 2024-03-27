from django.contrib import admin

from .models import Country, Language, Book


class CountryAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'country', 'language', 'view_year', 'pages']

    @admin.display(description='year')
    def view_year(self, obj):
        return f"{abs(obj.year)} B.C." if obj.year < 0 else obj.year


admin.site.register(Country, CountryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Book, BookAdmin)
