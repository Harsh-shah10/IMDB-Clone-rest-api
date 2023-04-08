from django.contrib import admin

# importing model
from watchlist_app.models import WatchList,StreamingPlatform,Review,Genre

# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamingPlatform)
admin.site.register(Review)
admin.site.register(Genre)
