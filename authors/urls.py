from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('login/', views.AuthorsLogin.as_view(), name='login'),
    path('logout/', views.AuthorsLogout.as_view(), name='logout'),

    path('register/', views.AuthorsRegister.as_view(), name='register'),
    path('feed/', views.AuthorsFeed.as_view(), name='feed'),
    path('search/', views.AuthorsSearch.as_view(), name='search'),
    path('profile/<int:pk>', views.ProfilePage.as_view(), name='profile'),
    path('followers/<int:pk>/<str:action>',
         views.ProfileFollowMethods.as_view(), name='followers')
]
