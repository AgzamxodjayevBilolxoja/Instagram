from django.contrib import admin

from reels.models import Reel, Like, Comment

admin.site.register(Reel)
admin.site.register(Like)
admin.site.register(Comment)