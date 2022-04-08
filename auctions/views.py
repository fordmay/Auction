from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import ListingForm, BidForm
from .models import User, AuctionListing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(active=True),
        "page_name": "Active Listings"
    })


def listing_page(request, id_listing):
    listing = AuctionListing.objects.get(pk=id_listing)

    if request.user.is_authenticated:

        if Bid.objects.filter(listing=id_listing).exists():
            bid = Bid.objects.filter(listing=id_listing).last().bid
        else:
            bid = AuctionListing.objects.get(pk=id_listing).starting_bid

        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "bid": bid,
            "check_watchlist": request.user.watchlist_listings.filter(pk=id_listing).exists(),
            "bid_form": BidForm()
        })
    else:
        return render(request, "auctions/listing_page.html", {
            "listing": listing
        })


# add and remove listing to watchlist
def post_watchlist(request, id_listing):
    listing = AuctionListing.objects.get(pk=id_listing)
    if request.method == "POST":
        if request.user.watchlist_listings.filter(pk=id_listing).exists():
            request.user.watchlist_listings.remove(listing)
        else:
            request.user.watchlist_listings.add(listing)
    return HttpResponseRedirect(reverse("listing_page", args=(id_listing,)))


def post_bid(request, id_listing):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        # check whether it's valid:
        if bid_form.is_valid():
            # process the data in form.cleaned_data as required
            get_bid = bid_form.cleaned_data["bid"]
            # starting_bid = AuctionListing.objects.get(pk=id_listing)

            if Bid.objects.filter(listing=id_listing).exists():
                bid = Bid.objects.filter(listing=id_listing).last().bid
            else:
                bid = AuctionListing.objects.get(pk=id_listing).starting_bid

            if get_bid > bid:
                # save to bid
                bid = bid_form.save(commit=False)
                bid.owner = User.objects.get(username=request.user)
                bid.listing = AuctionListing.objects.get(pk=id_listing)
                bid.save()
                # save to current_price
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("listing_page", args=(id_listing,)))
            else:
                messages.add_message(request, messages.WARNING, "Starting bid can't be lower than 0.")
                return HttpResponseRedirect(reverse("listing_page", args=(id_listing,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(id_listing,)))


def categories(request):
    category_quantity = []
    for category in AuctionListing.CATEGORIES:
        quantity = AuctionListing.objects.filter(category=category[0], active=True).count()
        new_list = [category[1], quantity]
        category_quantity.append(new_list)
    if AuctionListing.objects.filter(category="", active=True):
        new_list = ["No Category", AuctionListing.objects.filter(category="", active=True).count()]
        category_quantity.append(new_list)
    return render(request, "auctions/categories.html", {
        "category_quantity": category_quantity
    })


def filter_by_category(request, category_name):
    category_id = ""
    for category in AuctionListing.CATEGORIES:
        if category[1] == category_name:
            category_id = category[0]
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(category=category_id, active=True),
        "page_name": f"Filter by: {category_name}"
    })


@login_required(login_url="/login")
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist_listings.all(),
        "page_name": "Watchlist"
    })


@login_required(login_url="/login")
def create_listing(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ListingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            starting_bid = form.cleaned_data["starting_bid"]
            if starting_bid >= 0:
                listing = form.save(commit=False)
                listing.owner = User.objects.get(username=request.user)
                listing.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.add_message(request, messages.WARNING, "Starting bid can't be lower than 0.")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")