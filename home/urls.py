from django.urls import path
from .views import (PostListView, PostSearchView, PostByAuthorView, PostByDateView, PostDetailView, PostCreateView,
                    PostUpdateView, PostDeleteView, CommentDeleteView, register_validate)

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('ajax/register_validate', register_validate, name='register-validate'),
    path('post/user/<str:username>/', PostByAuthorView.as_view(), name="author-post"),
    path('post/date/<int:year>/<int:month>/', PostByDateView.as_view(), name="date-post"),
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<str:slug>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
