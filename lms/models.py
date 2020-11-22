from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import re
from django.core.validators import RegexValidator


class Book(models.Model):
    patten = re.compile(r'[A-Z]\d{2,9}')
    BookID = models.CharField(max_length=64, primary_key=True,
                              validators=[RegexValidator(regex=patten)],
                              help_text='The format is one character and 2 to 9 digits')
    Title = models.TextField()
    Language = models.TextField()
    Author = models.TextField()
    Publisher = models.TextField()
    PublishDate = models.DateField()
    ISBN = models.CharField(max_length=64, unique=True)

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
            y = Reserve.objects.filter(q1 & q2).values_list()[:1].get()[3]
            return User.objects.filter(id = y).values_list("username", flat=True)[0]
        else:
            return ""


class BookInstance(models.Model):
    BookInstanceID = models.CharField(max_length=64, unique=True, primary_key=True)
    BookID = models.ForeignKey(Book, db_column='BookID', on_delete=models.PROTECT)
    BOOK_INSTANCE_STATUS = (
        ('Maintenance', 'Maintenance'),
        ('On Loan', 'On Loan'),
        ('Available', 'Available'),
    )
    Status = models.CharField(max_length=15, choices=BOOK_INSTANCE_STATUS, default='a')

    def __str__(self):
        return f'{self.BookInstanceID} ({self.BookID.Title})'

    def DueDate(self):
        q1 = Q(BookInstanceID = self.BookInstanceID)
        q2 = Q(ReturnDate__isnull=True)
        y = BorrowRecord.objects.filter(q1 & q2).values_list('DueDate', flat=True)
        if self.Status == "On Loan":
            return y[0]
        else:
            return ""

    def Username(self):
        q1 = Q(BookInstanceID = self.BookInstanceID)
        q2 = Q(ReturnDate__isnull=True)
        x = BorrowRecord.objects.filter(q1 & q2).values_list('UserID__username', flat=True)
        if self.Status == "On Loan":
            return x[0]
        else:
            return ""

class BorrowRecord(models.Model):
    BorrowID = models.AutoField(primary_key=True)
    BookInstanceID = models.ForeignKey(BookInstance, db_column='BookInstanceID', on_delete=models.PROTECT)
    UserID = models.ForeignKey(User, db_column='UserID', on_delete=models.PROTECT)
    BorrowDate = models.DateField()
    DueDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.BorrowID} ({self.BookInstanceID}-{self.UserID})'


class Reserve(models.Model):
    ReserveID = models.AutoField(primary_key=True)
    BookID = models.ForeignKey(Book, db_column='BookID', on_delete=models.PROTECT)
    BookInstanceID = models.ForeignKey(BookInstance, db_column='BookInstanceID', on_delete=models.PROTECT, blank=True,
                                       null=True)
    UserID = models.ForeignKey(User, db_column='UserID', on_delete=models.PROTECT)
    ReserveDate = models.DateField()
    ReleaseDate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.ReserveID} ({self.BookID}-{self.UserID})'

    def Waiting(self):
        q1 = Q(BookID=self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        q3 = Q(UserID=self.UserID)
        y = Reserve.objects.filter(q1 & q2 & q3).values_list()[:1].get()[0]
        q4 = Q(ReserveID__lt=y)
        return Reserve.objects.filter(q1 & q2 & q4).count() + 1

# Create your models here.
