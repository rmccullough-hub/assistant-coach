from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_page, name='news'),
	path('news/<int:id>/', views.news_page, name='archive'),
	path('predictions/', views.predictions_page, name='predictions'),
	path('rankings/', views.rankings_page, name='rankings'),
	path('update/', views.update_page, name='update'),

]