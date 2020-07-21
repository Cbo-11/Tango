from django.contrib import admin

# Register your models here.
from rango.models import Catagory, Page

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','catagory', 'url')

admin.site.register(Catagory,CatagoryAdmin)
admin.site.register(Page, PageAdmin)



