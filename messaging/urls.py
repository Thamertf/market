from django.urls import path
from messaging.views import *



urlpatterns = [
    path('', inbox, name="inbox"),
    path('new/<username>', NewConversation, name="new-conversation"),
    path('directs/<username>', Directs, name="directs"),
    path('send/', SendDirect, name="send-direct"),
    path('loadmore/', LoadMore, name='loadmore'),
    path('search/', UserSearch, name='user-search'),

]