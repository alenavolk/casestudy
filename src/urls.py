"""
URL configuration for Case Study project.
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from src.books.views import main, BookViewSet


router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='Book')

urlpatterns = [
    path('', main),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
