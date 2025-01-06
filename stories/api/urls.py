from django.urls import path

from stories.api.views import add_stories_view, get_stories_view, del_stories_view

urlpatterns = [
    path('add/', add_stories_view),
    path('', get_stories_view),
    path('del/<int:pk>/', del_stories_view),
]