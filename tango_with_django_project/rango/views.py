# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page

def encode(item):
	return item.replace(' ', '_')

def decode(item):
	return item.replace('_', ' ')

def index(request):
	# Obtain the context from the HTTP request
	context = RequestContext(request)
	# Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.

	category_list = Category.objects.order_by('-likes')[:5]
	for category in category_list:
		#category.url = category.name.replace(' ', '_')
		category.url = encode(category.name)
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories' : category_list, 'pages' : page_list}
	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	context_dict = {'django' : 'DJANGO'}
	return render_to_response('rango/about.html', context_dict, context)

def category(request, category_name_url):
	context = RequestContext(request)

	category_name = decode(category_name_url) #category_name_url.replace('_', ' ')
	context_dict = {'category_name' : category_name}
	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render_to_response('rango/category.html', context_dict, context)