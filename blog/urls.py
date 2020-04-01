from django.urls import path, include
from . import views

# Contains All urls related to blog app

app_name = 'blog'

urlpatterns = [
    path('',views.post_list, name='blog_list'),
    path('tags/<slug:tag_slug>/',views.post_list, name='blog_list_by_tags'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
