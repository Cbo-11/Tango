from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render 
from rango.models import Catagory, Page

def index(request):
    #Query the database for a list of all catergories 
    #order by number of likes 
    #retrieve only the top 5 results
    catagory_list = Catagory.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': catagory_list, 'pages': page_list}
    
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

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
