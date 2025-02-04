from django.urls import path
from .views import google_login, auth_callback, get_videos, get_comments, post_comment, like_all_comments, delete_all_comments

urlpatterns = [

    path('google-login/', google_login, name='google-login'),
    path('auth-callback/', auth_callback, name='auth-callback'),
    path('get-videos/', get_videos, name='get-videos'),
    path('get-comments/<str:video_id>/', get_comments, name='get-comments'),
    path('post-comment/<str:video_id>/', post_comment, name='post-comment'),
    path('like-all-comments/<str:video_id>/', like_all_comments, name='like-all-comments'),
    path('delete-all-comments/<str:video_id>/', delete_all_comments, name='delete-all-comments'),

]