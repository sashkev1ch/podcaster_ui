from django.urls import path


from podcaster_ui.episode import views


urlpatterns = [
    path("<int:episode_id>/view/", views.EpisodeView.as_view(), name="episode"),
    path("<int:episode_id>/download/", views.DownloadEpisodeView.as_view(), name="download_episode"),
]
