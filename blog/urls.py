from django.urls import path, include
from . import views

# Contains All urls related to blog app

app_name = 'blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='blog_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
