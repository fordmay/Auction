from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    CATEGORIES = [
        ('EL', 'Electronics'),
        ('TO', 'Toys'),
        ('FA', 'Fashion'),
        ('FU', 'Furniture'),
        ('HO', 'Home'),
        ('TR', 'Transports'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, max_length=400)
    current_bid = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=2, choices=CATEGORIES, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    watchlist_users = models.ManyToManyField(User, blank=True, related_name="watchlist_listings")

    def __str__(self):
        return f"LISTING id:{self.pk}, owner:{self.owner}, category:{self.get_category_display()}, active:{self.active}"


class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"BID id:{self.pk}, owner:{self.owner} - ${self.bid}, listing:{self.listing}"


class Comments(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=400)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"COMMENT id:{self.pk}, author:{self.author}, comment:{self.comment[:50]}, listing:{self.listing}"
