from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='blog-post-list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='blog-post-detail'),
    path('<int:post_id>/share/', views.post_share, name='post-share'),
    path('<int:post_id>/comment/', views.comment_post, name='post_comment'),
]