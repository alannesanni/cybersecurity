from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/', views.polls, name='polls'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('add_poll/', views.add_poll, name='add_poll'),
    path('<int:question_id>/add_note/', views.add_note, name='add_note'),
]