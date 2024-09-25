from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('post/', views.PostsView.as_view(), name='post'),
    path('post/<int:pk>', views.PostsView.as_view(), name='post'),
    path('delete_tweet/<int:pk>', views.PostDelete.as_view(), name='delete'),
    path('add_comment/<int:pk>', views.CommentView.as_view(), name='add_comment')
]
