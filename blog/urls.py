from django.contrib import admin
from django.urls import path
from . import views
from .views import PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView, upload_file

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('filter/',views.filter, name='blog-filter'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/create/',upload_file, name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name='post-delete'),
    path('user/<username>', UserPostListView.as_view(), name='user-posts'),
]