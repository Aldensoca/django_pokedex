from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#Caso eu resolva fazer uma views alternativa usando os dados direto da API (Para fins de comparação)
    #from . import alternativeviews
    #alternativeviews = False

urlpatterns = [
    path('', views.pokedex, name='Pokedex'),
    path('<str:identifier>/', views.pokemon_entry, name='PokemonEntry') #Entry de cada pokemon na pokedex  
]