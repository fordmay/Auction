from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:id_listing>", views.listing_page, name="listing_page"),
    path("categories", views.categories, name="categories"),
    # use index.html
    path("categories/<str:category_name>", views.filter_by_category, name="filter_by_category"),
    # use index.html
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id_listing>/post_watchlist", views.post_watchlist, name="post_watchlist"),
    path("listing/<int:id_listing>/post_bid", views.post_bid, name="post_bid"),
    path("listing/<int:id_listing>/close_auction", views.close_auction, name="close_auction"),
]
