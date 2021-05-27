from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('movie_search/', views.movie_search),
    path('reviews/', views.reviews),
    path('reviews/<int:review_pk>/', views.review_update_delete),
    path('reviews/detail/<int:review_pk>/', views.review_detail),
    path('recommended_movies/', views.recommended_movies),
    path('reviews/detail/<int:review_pk>/comments/', views.comments),
    path('reviews/detail/<int:review_pk>/comments/<int:comment_pk>', views.comment_delete),
    path('recommended_movies/clear/', views.recommend_clear),
]
