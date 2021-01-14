from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('update/', views.update_page),
	path('articles/', views.api_articles),
	path('players/', views.api_players),
	path('filter/', views.api_filter),
	path('predictions/', views.api_predict),
]