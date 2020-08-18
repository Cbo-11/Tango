from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, redirect 
from rango.models import Catagory, Page, UserProfile
from rango.forms import CatagoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
import json
import urllib.parse
import urllib.request



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
        pages = Page.objects.filter(catagory=catagory).order_by('-views')
        context_dict['pages']= pages
        context_dict['catagory']=catagory
    except Catagory.DoesNotExist:
        context_dict['pages']= None
        context_dict['catagory']= None

    context_dict['query'] = catagory.name


    result_list = []
    if request.method == "POST":
        query= request.POST['query'].strip()

        if query:
            result_list = run_query(query)
            context_dict['query'] = query
            context_dict['result_list'] = result_list

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

def track_url(request):
    page_id= None
    url = '/rango/'
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page=Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['catagory_id']
        likes= 0
        if cat_id:
            cat = Catagory.objects.get(id=int(cat_id))
            likes= cat.likes +1
            cat.likes= likes
            cat.save()
    return HttpResponse(likes)   

def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
    # Run our Webhose search function to get the results list!
            result_list = run_query(query)
    return render(request, 'rango/search.html', {'result_list': result_list})
  

@login_required
def register_profile(request):
    form= UserProfileForm(request.POST, request.FILES)
    if form.is_valid():
        user_profile= form.save(commit=False)
        user_profile.user = request.user
        user_profile.save()

        return redirect('index')
    else: 
        print(form.errors)
    context_dict = {'form':form}

    return render(request, 'rango/profile_registration.html', context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance= userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form':form})

@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'rango/list_profiles.html', {'userprofile_list': userprofile_list})

def get_catagory_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Catagory.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_catagory(request):
    cat_list = []
    starts_with = ''

    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_catagory_list(8, starts_with)

    return render(request, 'rango/cats.html', {'cats': cat_list})

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.get['catagory_id']
        url = request.get['url']
        title = request.get['title']

        if cat_id:
            catagory = Catagory.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(catagory=catagory,title=title, url=url)
            pages = Page.objects.filter(catagory=catagory).order_by('-views')

            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)



    