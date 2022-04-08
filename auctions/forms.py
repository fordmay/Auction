from django.forms import ModelForm, Textarea, TextInput, URLInput, NumberInput, Select

from .models import AuctionListing, Bid


class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_bid', 'image', 'category']

        labels = {
            'current_bid': 'Starting bid',
            'image': 'Image URL'
        }

        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'current_bid': NumberInput(attrs={'class': 'form-control'}),
            'image': URLInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

        labels = {
            'bid': ''
        }
        widgets = {
            'bid': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bid'})
        }
