from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('orcamento/', views.orcamento, name='orcamento'),
    path('servicos/', views.servicos, name='servicos'),
    path('sobre/', views.sobre, name='sobre'),
    path('api/salvar-orcamento/', views.salvar_orcamento, name='salvar_orcamento'),
]