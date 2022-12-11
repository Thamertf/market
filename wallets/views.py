from django.shortcuts import render
from monero.wallet import Wallet  
from monero.backends.jsonrpc import JSONRPCWallet  
from monero.daemon import Daemon  
from monero.address import address  
from .utils import *
from .forms import *
# Encryption and decryption
from cryptography.fernet import Fernet  
import numpy  

import os  
import json  















def wallet(request):	




	# Traffic wallet through TOR
	daemon = Daemon(host="http://singapore.node.xmr.pm:28081")  
	wallet = Wallet(JSONRPCWallet(port=28088))
	 
	context = {
	'wallet':wallet
	}


	return render(request, 'auctions/wallet.html', context)


	# Do a try-catch block so that a high fee won't cancel the order.
	# Ideally, tell the user how much the fee is and what amount will actually send.
	# If amount sending is more than balance, cancel transaction and just redirect user back home, saying that they don't have enough $$$.







