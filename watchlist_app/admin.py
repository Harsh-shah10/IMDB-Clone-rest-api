from django.contrib import admin

# importing model
from watchlist_app.models import WatchList,StreamingPlatform,Review,Genre,TicketSale

# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamingPlatform)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(TicketSale)
