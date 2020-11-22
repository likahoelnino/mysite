from lms.models import *
from django import forms
import re
from django.core.exceptions import ValidationError


class BookInstanceModelForm(forms.ModelForm):
    def clean_Status(self):
        data = self.cleaned_data['Status']
        initial_data = self.initial['Status']
        if self.has_changed():
            if initial_data == 'Available':
                if data == 'On Loan':
                    raise ValidationError("Invalid Status (Current status: Available).")
            elif initial_data == 'On Loan':
                raise ValidationError("Invalid Status (Current status: On Loan).")
            elif initial_data == 'Maintenance':
                if data != 'Suspended':
                    raise ValidationError("Invalid Status (Current status: Maintenance).")
            elif initial_data == 'Suspended':
                if data == 'On Loan':
                    raise ValidationError("Invalid Status (Current status: Suspended).")
        return data

    class Meta:
        BOOK_INSTANCE_STATUS = (
            ('Maintenance', 'Maintenance'),
            ('On Loan', 'On Loan'),
            ('Available', 'Available'),
            ('Suspended', 'Suspended'),
        )

        model = BookInstance
        fields = '__all__'
        widgets = {
            'BookInstanceID': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'BookID': forms.TextInput(attrs={'class': 'form-group col-md-8'}),
            'Status': forms.Select(choices=BOOK_INSTANCE_STATUS, attrs={'class': 'form-group col-md-8'}),
        }
        labels = {
            'BookInstanceID': 'Book Instance ID',
            'BookID': 'Book ID',
            'Status': 'Status',
        }


class BookModelForm(forms.ModelForm):
    def clean_BookID(self):
        data = self.cleaned_data['BookID']
        patten = re.compile(r'[A-Z]\d{2,9}')
        if not(patten.match(data)):
            raise ValidationError("Invalid date - not follow the format (r'[A-Z]\\d{2,9}')")
        return data

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
        help_texts = {
            'BookID': 'e.g.: B001',
        }
