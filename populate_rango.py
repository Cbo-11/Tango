import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'Tango.settings')

import django
django.setup()
from rango.models import Catagory, Page

def populate():

    python_pages = [
        {"title": "Offical Python Tutorial",
        "url": "http://docs.python.org/2/tutorial/"},
         {"title": "How to Think like a Computer Scientist",
        "url": "http://www.greenteapress.com/thinkpython/"},
         {"title": "Learn Python in 10 Minutes",
        "url": "http://www.korokithakis.net/tutorials/python/"}
    ]

    django_pages = [
        {"title": "Offical Django Tutorial",
        "url": "http://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
        "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
        "url": "http://www.tangowithdjango.com/"}
    ]

    other_pages = [
        {"title": "Bottle",
        "url": "http://www.bottlepy.org/docs/dev/"},
        {"title": "Flask",
        "url": "http://flask.pocoo.org"}
    ]

    cat = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 64, "likes": 32},
        "Other Framworks": {"pages": other_pages, "views": 32, "likes": 16}
    }
    

    for cat, cat_data in cat.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        for p in cat_data["pages"]:
            add_page(c,p["title"],p["url"])

    for c in Catagory.objects.all():
        for p in Page.objects.filter(catagory=c):
            print("-{0}-{1}".format(str(c),str(p)))
    
def add_page(cat,title,url,views=0):
    p = Page.objects.get_or_create(catagory = cat, title = title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,views,likes):
    c = Catagory.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
    
if __name__ == '__main__':
    print("Starting rango population script...")
    populate()