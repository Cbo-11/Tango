from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render 

def index(request):
    #construct a dictrionary to pass to the template 
    #not the boldmessage is the same as in the template 
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #Return a rendered response to the client 
    #we make use of a shortcyt function to make life easier 
    #not the first parameter is the templaste
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')