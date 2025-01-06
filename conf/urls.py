from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.api.urls')),
    path('stories/', include('stories.api.urls')),
    path('reels/', include('reels.api.urls')),
]
