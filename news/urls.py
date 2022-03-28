from django.urls import path
from . import views 

urlpatterns = [
    path('', views.NewsCreateListView.as_view(), name='news'),
    path('<int:news_id>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('user/<int:user_id>/news/', views.UserNewsView.as_view(), name='users_news'),
    path('<int:news_id>/vote/', views.NewsVoteView.as_view(), name='vote'),
    path('<int:news_id>/comment/', views.NewsCommentView.as_view(), name='comment'),
    
]
