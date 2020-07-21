from django import forms
from rango.models import Page, Catagory

class CatagoryForm(forms.ModelForm):
    name= forms.CharField(max_length=128,
            help_text="Please enter the catagory name.")
    views= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug= forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model= Catagory
        fields= ('name',)


class PageForm(forms.ModelForm):
    title= forms.CharField(max_length=128,
        help_text="Please enter the title of the page.")
    url= forms.URLField(max_length=200,
        help_text= "Please enter the URL of the page.")
    views= forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model= Page
        exclude= ('catagory',)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url= cleaned_data.get('url')

        if url and not url.startswith('htp://'):
            url= 'http://' + url
            cleaned_data['url' = url]
            
            return cleaned_data