from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("create_poker_session/", views.create_poker_session, name="create_poker_session"),
    path("join_poker_session/", views.join_poker_session, name="join_poker_session"),
    path("poker_session/<int:pk>/", views.poker_session, name="poker_session"),
    path("vote/<int:poker_session_id>/<card>", views.vote, name="vote"),
]
