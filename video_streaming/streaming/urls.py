from django.urls import path
from streaming import views,video_streaming

# app_name = "streaming"

urlpatterns = [
    path("", views.VideoListView.as_view(), name = "video_list"),
    # path("", views.index),
    # path("video/", video_streaming.play_video),
    # path('video_feed/', video_streaming.video_feed, name='video_feed'),
    path("signup/",views.signup, name="signup"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("create_video/",views.create_video,name="create_video"),
    path("del/<int:video_id>/",views.delete_video,name="create_video"),
    path("edit/<int:video_id>/",views.edit_video,name="edit_video"),
    path('video_feed/<int:video_id>/', video_streaming.video_stream, name='video_feed'),
    path('update_video/<int:video_id>/',views.update_video,name="update_video")
]
