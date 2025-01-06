from django.urls import path

from users.api.views import register_stage1_view, register_stage2_view, register_stage3_view, login_view, \
    update_user_view, logout_view, delete_view, subscribe_view

urlpatterns = [
    path('register1/', register_stage1_view),
    path('register2/', register_stage2_view),
    path('register3/', register_stage3_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('delete/', delete_view),
    path('update/', update_user_view),
    path('subscribe/<int:pk>/', subscribe_view)
]