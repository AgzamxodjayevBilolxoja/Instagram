from django.urls import path

from reels.api.views import(
    add_reels_view,
    get_reels_view,
    del_reels_view,
    add_likes_view,
    add_comment_view,
    del_comment_view
)

urlpatterns = [
    path('add/', add_reels_view),
    path('', get_reels_view),
    path('del/<int:pk>/', del_reels_view),
    path('like/<int:pk>/', add_likes_view),
    path('comment/add/<int:pk>/', add_comment_view),
    path('comment/del/<int:pk>/', del_comment_view),
]