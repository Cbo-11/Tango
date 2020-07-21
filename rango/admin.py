from django.contrib import admin

# Register your models here.
from rango.models import Catagory, Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','catagory', 'url')

admin.site.register(Catagory)
admin.site.register(Page, PageAdmin)



