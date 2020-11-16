from lms.models import *
from django import forms

class BookInstanceModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = '__all__'
        widgets = {
            'BookInstanceID': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'BookID': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Status': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
        }
        labels = {
            'BookInstanceID': 'Book Instance ID',
            'BookID': 'Book ID',
            'Status': 'Status',
        }

class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'BookID': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Title': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Language': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Author': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Publisher': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'PublishDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-group col-md-8'}),
            'ISBN': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
        }
        labels = {
            'BookID': 'Book ID',
            'Title': 'Title',
            'Language': 'Language',
            'Author': 'Author',
            'Publisher': 'Publisher',
            'PublishDate': 'PublishDate',
            'ISBN': 'ISBN',
        }
