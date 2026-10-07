from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.books, name='books'),
    path('sobre/', views.about, name='about'),
]