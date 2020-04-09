from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='words-home'),
    path('level/', views.level, name='words-level'),
    path('about/', views.about, name='words-about'),
    path('allwords/<int:level>/', views.AllWordsListView.as_view(), name='words-all'),
    path('masteredwords/<int:level>/', views.MasteredWordsListView.as_view(), name='words-mastered'),
    path('reviewedwords/<int:level>/', views.ReviewedWordsListView.as_view(), name='words-reviewed'),
    path('search/', views.SearchWordsListView.as_view(), name='words-search')
]
