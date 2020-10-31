from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_page, name='news'),
	path('predictions/', views.predictions_page, name='predictions'),
	path('rankings/', views.rankings_page, name='rankings'),

]