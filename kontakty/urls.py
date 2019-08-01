from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:k_id>/edycja/', views.edycja, name='edycja'),
    # ex: /polls/5/results/
    path('<int:k_id>/dodajnumer/', views.dodajnumer, name='dodajnumer'),
    # ex: /polls/5/vote/
    path('<int:k_id>/dodajmail/', views.dodajmail, name='dodajmail'),
    path('dodajkontakt/', views.dodajkontakt, name='dodajkontakt'),
    path('szukaj.html', views.szukaj, name='szukaj'),
    path('<int:id>/usun/', views.delete, name='delete'),
]