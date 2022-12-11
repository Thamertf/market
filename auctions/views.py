from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from .models import *
from django.utils import timezone
from decimal import Decimal
from django.http import Http404
from django.db import models
from dateutil import tz
import pytz
from django.contrib import messages
from .forms import *
from .decorators import *
from .filters import *
from django.contrib.auth.models import Group
from django.urls import resolve



def index(request):
    listings = ActiveListing.objects.filter(active=True).order_by('-id')

    return render(request, "auctions/index.html", {
        'listings': listings, 'active': True
    })

def inactive_listing(request):
    listings = ActiveListing.objects.filter(active=False).order_by('-id')

    return render(request, "auctions/index.html", {
        'listings': listings, 'active': False
    })



@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'auctions/login.html', context)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'auctions/register.html', context)



def settings(request, username=None):

    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)

    context = {'account': account}
    return render(request, "auctions/settings.html", context)



def profile(request, username=None):

    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)

    context = {'account': account}
    return render(request, "auctions/userprofile.html", context)


def vendor(request, username=None):

    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)

    context = {'account': account}
    return render(request, "auctions/vendor.html", context)







@login_required(login_url='login')
def create(request):
    form = ActiveListingForm()
    if request.method == 'POST':
        form = ActiveListingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create.html")

    context = {'form': form}
    return render(request, "auctions/create.html", context)


def item(request, item_id, username=None):
    # Current logged in user
    if username:
        user = get_object_or_404(User, username=username)

    else:
        user = request.user

    # Select (get) the item from the database
    item = ActiveListing.objects.get(id=item_id)

    # Check if the item and the username are in the watchlist database (same row)
    itemIsInWatchlist = WatchList.objects.filter(items=item_id) & WatchList.objects.filter(user=user)

    # Change to the correct text on the add/remove watchlist button
    watchlistBtnMsg = ''
    if itemIsInWatchlist.exists():
        watchlistBtnMsg = 'Remove Watchlist'
    elif itemIsInWatchlist.exists() == False:
        watchlistBtnMsg = 'Add Watchlist'
   


    # All the bids for the selected item
    bids = Bids.objects.filter(item=item_id)

        

    # All the comments for the selected item
    comments = Comments.objects.filter(item=item_id)


    return render(request, 'auctions/item.html', {
        'item': item, 'user': user, 'watchlistBtnMsg': watchlistBtnMsg,
        'comments': comments, 'bids': bids,
        
        
    })


def createWatchList(request):
    if request.method == 'POST':
        addWatchlist = WatchList()
        addWatchlist.user = request.user
        itemId = request.POST.get('items_id')
        addWatchlist.items = ActiveListing.objects.get(id=itemId)

        # Check if the item and the username are in the watchlist database (same row)
        itemIsInList = WatchList.objects.filter(items=addWatchlist.items).filter(user=addWatchlist.user)
        # itemIsInList = WatchList.objects.filter(items=addWatchlist.items) & WatchList.objects.filter(user=addWatchlist.user)
        if itemIsInList.exists() == False:
            # Check if the user is logged in
            try:
                # If logged in, it'll save and add to the watchlist
                User.objects.get(username=addWatchlist.user)
                addWatchlist.save()
                return HttpResponseRedirect(reverse('item',args=[itemId]))
            except User.DoesNotExist:
                # If user is not logged in, it won't save it
                return HttpResponseRedirect(reverse('item',args=[itemId]))
        elif itemIsInList.exists():
            itemIsInList.delete()
            return HttpResponseRedirect(reverse('item',args=[itemId]))

    return HttpResponseRedirect(reverse("index"))


def watchlist(request):
    user = request.user
    msg = ''

    itemIsInWatchlist = WatchList.objects.filter(user=user)

    if itemIsInWatchlist.exists() == False:
        msg = 'Your watchlist is empty.'        

    return render(request, "auctions/watchlist.html", {
        'items': itemIsInWatchlist, 'msg': msg
    })



# List all categories
def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        'categories':categories
    })


# Items within the specified category
def category(request, slug):
    # Filter all items which belongs to the category
    if slug:
        try:
            items = ActiveListing.objects.filter(category__slug=slug).order_by('-id')
            # Set() converted to from queryset to list and extract the title
            title = list(items)[0]
        except ActiveListing.DoesNotExist:
            raise Http404
        except ActiveListing.MultipleObjectsReturned:
            items = ActiveListing.objects.filter(category__slug=slug).order_by('-id')
            # Set() converted to from queryset to list and extract the title
            title = list(items)[0]
        except:
            raise Http404

    return render(request, "auctions/categories.html", {
        'title': title, 'items':items
    })

# Add and save comments
def comment(request):
    if request.method == 'POST':
        if request.POST.get('comment'):
            # A small server side form validation only for the length of the inputs
            if len(request.POST.get('comment')) < 512:
                create = Comments()
                itemId = request.POST.get('item_id')
                create.user = request.user
                create.item = ActiveListing.objects.get(id=itemId)
                create.comment = request.POST.get('comment')
                create.save()

    return HttpResponseRedirect(reverse('item',args=[itemId]))


def bid(request):
    if request.method == 'POST':
        # Create a new bid
        if request.POST.get('bid'):
            # A small server side form validation only for the length of the inputs
            if len(request.POST.get('bid')) < 10:
                create = Bids()
                user = request.user
                itemId = request.POST.get('item_id')
                newBid = Decimal(request.POST.get('bid'))
                item = ActiveListing.objects.get(id=itemId)
                # Get the starting price
                price = ActiveListing.objects.filter(id=itemId).values('price')
                startingPrice = price[0]['price']
                # Get the highest bid
                getMaxBid = Bids.objects.filter(item_id=itemId).aggregate(Max('bid'))
                # Extract the highest bid
                maxBid = getMaxBid['bid__max']

                # If a bid already exist
                if Bids.objects.filter(item_id=itemId).exists():
                    # Check if the new bid is higher than the highest bid and the starting price, and if the item is active
                    if newBid > maxBid and newBid > startingPrice and item.active == True:
                        create.user = user
                        create.item = ActiveListing.objects.get(id=itemId)
                        create.bid = newBid
                        create.save()

                        return HttpResponseRedirect(reverse('item',args=[itemId]))
                # If a bid is not exist yet
                else:
                    # Check if bid is higher than the starting price, and if the item is active
                    if newBid > startingPrice and item.active == True:
                        create.user = user
                        create.item = ActiveListing.objects.get(id=itemId)
                        create.bid = newBid
                        create.save()
                    
                    return HttpResponseRedirect(reverse('item',args=[itemId]))
        
        # Close and Open a bid
        if request.POST.get('activate'):
            itemId = request.POST.get('item_id')
            item = ActiveListing.objects.get(id=itemId)
            
            if item.active == True:
                item.active = False
                item.save()

            elif item.active == False:
                item.active = True
                item.save()
            
            return HttpResponseRedirect(reverse('item',args=[itemId]))

        if request.POST.get('activate'):
            itemId = request.POST.get('item_id')
            item = ActiveListing.objects.get(id=itemId)
            
            if item.active == True:
                item.active = False
                item.save()

            elif item.active == False:
                item.active = True
                item.save()
            
            return HttpResponseRedirect(reverse('item',args=[itemId]))

    return HttpResponseRedirect(reverse('index'))







@login_required(login_url='login')
def my_auctions(request):
    # Get all auctions by user, sorted by date
    my_auctions_list = ActiveListing.objects.all().filter(user=request.user).order_by('-price')




    template = loader.get_template('auctions/my_auctions.html')
    context = {
        'my_auctions_list': my_auctions_list,
    }
    return HttpResponse(template.render(context, request))



@login_required(login_url='login')
def vendorshop(request, username=None):
    # Get all auctions by user, sorted by date
    user = User.objects.get(username=username)
    shop_list = ActiveListing.objects.all().filter(user=user).order_by('-price')
    template = loader.get_template('auctions/vendorshop.html')




    context = {
        'shop_list': shop_list,
    }
    return HttpResponse(template.render(context, request))



def search(request):
    q = request.GET['q']
    listings = ActiveListing.objects.filter(title__icontains=q).order_by('-id')

    return render(request, "auctions/search.html", {
        'listings': listings
    })

