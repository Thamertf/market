from .models import *
from django.db.models import Min,Max
def get_filters(request):
	cats=ActiveListing.objects.distinct().values('category__name','category__id')
	data={
		'cats':cats,
	}
	return data