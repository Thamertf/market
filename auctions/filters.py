from django.db import models
import django_filters
from .models import ActiveListing
class ActiveListingFilter(django_filters.FilterSet):

	class Meta:
		model = ActiveListing
		fields = [
			'category'
		]
		filter_overrides = {
	    	models.CharField:{
	    		'filter_class' : django_filters.ChoiceFilter,
	    		'extra' : lambda f: {
	        		'widget' : 'forms.CheckboxInput'
		        }
		    }
		}