from django.urls import path, include


from podcaster_ui.channel import views


urlpatterns = [
    path("", views.AllChannelsView.as_view(), name="channels"),
    path("create/", views.CreateChannelView.as_view(), name="create_channel"),
    path("<int:channel_id>/update/", views.UpdateChannelView.as_view(), name="update_channel"),
    path("<int:channel_id>/delete/", views.DeleteChannelView.as_view(), name="delete_channel"),
    path("<int:channel_id>/view/", views.ChannelView.as_view(), name="view_channel"),
    path("<int:channel_id>/refresh/", views.RefreshChannelView.as_view(), name="refresh_channel"),
    path("<int:channel_id>/episodes/", include("podcaster_ui.episode.urls")),
]
