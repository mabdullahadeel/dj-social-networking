from . import views 
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('', views.post_comment_create_list_view, name='home_post_view'),
    path('post_reaction', views.like_unlike_view, name='like_unlike_view'),
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
]