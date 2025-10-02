from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/<str:session_id>/', views.results, name='results'),
    path('legacy/', views.legacy_index, name='legacy'),
]
