from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("inactive_listing", views.inactive_listing, name="inactive_listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("item<int:item_id>", views.item, name="item"),
    path("createwatchlist", views.createWatchList, name="createWatchList"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug:slug>/", views.category, name="category"),
    path("comment", views.comment, name="comment"),
    path('create/', views.create, name='create'),
    path('myauctions/', views.my_auctions, name="my_auctions"),
    path('vendorshop/<str:username>/', views.vendorshop, name="vendorshop"),
    path('settings/<str:username>/', views.settings, name="settings"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('vendor/<str:username>/', views.vendor, name="vendor"),


    

    # path('myauctions/', views.my_auctions, name='my_auctions'),
    # Example: /auctions/
    # Example: /auctions/5/
    # Example: /auctions/5/results/
    # path('<int:auction_id>/results/', views.results, name='results'),
    # Example: /auctions/5/bid/
]
