from django.forms import ModelForm, Textarea, TextInput, URLInput, NumberInput, Select

from .models import AuctionListing, Bid, Comments


class ListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'current_bid', 'image', 'category']
        labels = {'current_bid': 'Starting bid', 'image': 'Image URL'}
        widgets = {
            'title': TextInput(attrs={'class': 'form-control border-primary'}),
            'description': Textarea(attrs={'class': 'form-control border-primary'}),
            'current_bid': NumberInput(attrs={'class': 'form-control border-primary'}),
            'image': URLInput(attrs={'class': 'form-control border-primary'}),
            'category': Select(attrs={'class': 'form-control border-primary'}),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        labels = {'bid': ''}
        widgets = {
            'bid': NumberInput(attrs={'class': 'form-control border-primary', 'placeholder': 'Bid'})
        }


class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        labels = {'comment': ''}
        widgets = {
            'comment': Textarea(attrs={'class': 'form-control border-primary'})
        }
