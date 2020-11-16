from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User


class Book(models.Model):
    patten = re.compile(r'[A-Z]\d{2,9}')
    BookID = models.CharField(max_length=64, primary_key=True,
                              validators=[RegexValidator(regex=patten)],
                              help_text='The format is one character and 2 to 9 digits')
    Title = models.CharField(max_length=500)
    Language = models.CharField(max_length=100)
    Author = models.CharField(max_length=500)
    Publisher = models.CharField(max_length=500)
    PublishDate = models.DateField()
    ISBN = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f'{self.BookID} ({self.Title})'

    def Waiting(self):
        q1 = Q(BookID=self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        return Reserve.objects.filter(q1 & q2).count()

    def ReserveUser(self):
        q1 = Q(BookID=self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        if Reserve.objects.filter(q1 & q2).count() > 0:
            return Reserve.objects.filter(q1 & q2).values_list()[:1].get()[3]
        else:
            return ""


class BookInstance(models.Model):
    patten = re.compile(r'[A-Z]\d{2,9}[.]\d{2,4}')
    BookInstanceID = models.CharField(max_length=64, primary_key=True,
                                      validators=[RegexValidator(regex=patten)],
                                      help_text='the format is book id with a dot and 2 - 4 digits (i.e.: B001.01)')
    BookID = models.ForeignKey(Book, db_column='BookID', on_delete=models.PROTECT)
    BOOK_INSTANCE_STATUS = (
        ('Maintenance', 'Maintenance'),
        ('On Loan', 'On Loan'),
        ('Available', 'Available'),
    )
    Status = models.CharField(max_length=15, choices=BOOK_INSTANCE_STATUS, default='a')

    def __str__(self):
        return f'{self.BookInstanceID} ({self.BookID.Title})'


class BorrowRecord(models.Model):
    BorrowID = models.AutoField(primary_key=True)
    BookInstanceID = models.ForeignKey(BookInstance, db_column='BookInstanceID', on_delete=models.PROTECT)
    id = models.ForeignKey(User, db_column='id', on_delete=models.PROTECT)
    BorrowDate = models.DateField()
    DueDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} ({self.BookInstanceID}-{self.id})'


class Reserve(models.Model):
    ReserveID = models.AutoField(primary_key=True)
    BookID = models.ForeignKey(Book, db_column='BookID', on_delete=models.PROTECT)
    BookInstanceID = models.ForeignKey(BookInstance, db_column='BookInstanceID', on_delete=models.PROTECT, blank=True,
                                       null=True)
    id = models.ForeignKey(User, db_column='id', on_delete=models.PROTECT)
    ReserveDate = models.DateField()
    ReleaseDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} ({self.BookID}-{self.id})'

# Create your models here.
