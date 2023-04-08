from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'genre_list'

    def __str__(self):
        return self.name

class StreamingPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)
    
    class Meta:
        db_table = 'streaming_platform'
        
    def __str__(self):
        return self.name
        

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    storyline = models.CharField(max_length=300)
    year = models.IntegerField(null=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre)

    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name="WatchList")
    
    class Meta:
        db_table = 'watch_list'
        
    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='all_review')

    class Meta:
        db_table = 'all_review'
        
    def __str__(self):
        return 'Rating : ' + str(self.rating) + ' : ' + self.watchlist.title
     
class TicketSale(models.Model):
    name = models.CharField(max_length=50)
    movie = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_sales'
        
