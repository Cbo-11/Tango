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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


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

def register(request):
    #boolean value for telling the template whether 
    #the registeration was succesfful 
    #set false innitially then change in process 
    #True when registartion successful
    registered = False 

    #if its a HTTP POST, we're interested in processing the form data 
    if request.method == 'POST':
        #grab info from the raw data form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if both forms are valid 
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #Now we hash the password and update the user 
            user.set_password(user.password)
            user.save()

            #now sort the profile instance 
            #since we need to set the user attribute ourselves ,
            #set commit to false, this delats saving the model 

            profile = profile_form.save(commit=False)
            profile.user = user

            #did the user provide a profile pic 
            #if so then put it in the profile model 
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #save the user profile instance 
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else: 
        user_form = UserForm()
        profile_form = UserProfileForm
    return render(request,'rango/register.html', 
                    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        #gather user name and password provided, this infor is obtained 
        #from the login form
        #we us request.post.get['<variable>'] bacause the "".get() varaible returns none if the value 
        #does not exist while the get.[] will raise a key error exception 
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use django machinerty to attempt to see if the username/password combo is valid
        user = authenticate(username=username, password=password)

        #if we have a user object the details are correct 
        #if none then no user 
        if user:
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Finn account is disabled")
        else: 
            #bad login details so cant log in 
            print("invalid login details: {0},{1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        #the request is not HTTP POST, so display the login form 
        #likely to be an HTTP GET
        # no context variable to pass to template hence blank dict 
        return render(request,'rango/login.html',{})

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