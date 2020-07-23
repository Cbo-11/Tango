from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render 
from rango.models import Catagory, Page
from rango.forms import CatagoryForm, PageForm

def index(request):
    #Query the database for a list of all catergories 
    #order by number of likes 
    #retrieve only the top 5 results
    catagory_list = Catagory.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catagory_list, 'pages': page_list}
    
    return render(request, 'rango/index.html', context_dict)

def about(request):
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})

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
    