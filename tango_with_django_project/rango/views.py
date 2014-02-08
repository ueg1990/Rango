# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
	context = RequestContext(request)
	if request.method == 'POST':
		form.CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = decode_url(category_name_url)
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                # If we get here, the category does not exist.
                # We render the add_page.html template without a context dictionary.
                # This will trigger the red text to appear in the template!
                return render_to_response('rango/add_page.html', {}, context)

            # Also, create a default value for the number of views.
            page.views = 0

            # With this, we can then save our new model instance.
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response( 'rango/add_page.html',
            {'category_name_url': category_name_url,
             'category_name': category_name, 'form': form},
             context)