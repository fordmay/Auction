from django.forms import ModelForm, Textarea, TextInput, URLInput, NumberInput, Select

from .models import AuctionListing, Bid


class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_bid', 'image', 'category']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control w-75'}),
            'description': Textarea(attrs={'class': 'form-control w-75'}),
            'current_bid': NumberInput(attrs={'class': 'form-control w-75'}),
            'image': URLInput(attrs={'class': 'form-control w-75'}),
            'category': Select(attrs={'class': 'form-control w-75'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

        labels = {
            'bid': ''
        }
        widgets = {
            'bid': NumberInput(attrs={'class': 'form-control w-75', 'placeholder': 'Bid'})
        }
