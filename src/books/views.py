from django.core import exceptions
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets

from .models import Country, Language, Book
from .serializers import BookSerializer


def main(request):
    template = loader.get_template('main.html')
    context = {
        'library_name': "Random Books Library",
        'num_books': Book.objects.count()
    }
    return HttpResponse(template.render(context, request))


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        params = self.request.query_params
        country_name, language_name, order_by = (
            params.get('country'), params.get('language'), params.get('order_by')
        )
        if country_name:
            try:
                country = Country.objects.get(name=country_name)
            except Country.DoesNotExist:
                return Book.objects.none()
            else:
                queryset = queryset.filter(country=country)
        if language_name:
            try:
                language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                return Book.objects.none()
            else:
                queryset = queryset.filter(language=language)
        try:
            return queryset.order_by(order_by)
        except exceptions.FieldError:
            return queryset
