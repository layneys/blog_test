from django.urls import path
from .views import PostsListView, PostsCreateView, PostsUpdateView, PostDetailView

app_name = 'posts'

urlpatterns = [
    # path('', animals.index, name='index'),
    path('',
         PostsListView.as_view(),
         name='posts_list'),
    path('posts/<int:pk>/',
         PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/',
         PostsCreateView.as_view(),
         name='post_create'),
    path('posts/update/<int:item_pk>/',
         PostsUpdateView.as_view(),
         name='post_update'), ]
