from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render 
from rango.models import Catagory, Page
from rango.forms import CatagoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

def index(request):
    #Query the database for a list of all catergories 
    #order by number of likes 
    #retrieve only the top 5 results
    catagory_list = Catagory.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catagory_list, 'pages': page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context_dict)
    return response

def about(request):
    
    print(request.method)
    print(request.user)
    context_dict = {}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']


    response = render(request, 'rango/about.html', {})
    return response

def show_catagory(request,catagory_name_slug):
    context_dict = {}

    try:
        catagory = Catagory.objects.get(slug=catagory_name_slug)
        pages = Page.objects.filter(catagory=catagory)
        context_dict['pages']= pages
        context_dict['catagory']=catagory
    except Catagory.DoesNotExist:
        context_dict['pages']= None
        context_dict['catagory']= None
    return render(request, 'rango/catagory.html', context_dict)

@login_required
def add_catagory(request):
    form = CatagoryForm()

    #A HTTP POST?
    if request.method == 'POST':
        form = CatagoryForm(request.POST)

        #Have we got a valid form? 
        if form.is_valid():
            #Save the new category to the database
            form.save(commit=True)
            #Category saved 
            #direct back to index page
            return index(request)
        else:
            #the supplied form has errors 
            #print to terminal 
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, catagory_name_slug):
    try:
        catagory = Catagory.objects.get(slug=catagory_name_slug)
    except Catagory.DoesNotExist:
        catagory = Non

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if catagory:
                page= form.save(commit= False)
                page.catagory = catagory
                page.views = 0
                page.save()
                return show_catagory(request, catagory_name_slug)
        else:
            print(form.errors)
    context_dict= {'form': form, 'catagory': catagory}
    return render(request, 'rango/add_page.html', context_dict)


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    #if its been more than a dat since the last visit 
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        #update the last visit cookie now that we have updated the count 
        request.session['last_visit'] = str(datetime.now())
    else: 
        #set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie
    #update/set the visits cookie 
    request.session['visits'] = visits