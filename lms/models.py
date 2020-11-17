from django.db import models
from django.db.models import Q

class Book (models.Model):
    BookID = models.CharField(max_length=64, unique=True, primary_key = True)
    Title = models.TextField()
    Language = models.TextField()
    Author = models.TextField()
    Publisher = models.TextField()
    PublishDate = models.DateField()
    ISBN = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name

    def Waiting(self):
        q1 = Q(BookID = self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        return Reserve.objects.filter(q1 & q2).count()

    def ReserveUser(self):
        q1 = Q(BookID = self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        if Reserve.objects.filter(q1 & q2).count() > 0:
            return Reserve.objects.filter(q1 & q2).values_list()[:1].get()[3]
        else:
            return ""

class BookInstance (models.Model):
    BookInstanceID = models.CharField(max_length=64, unique=True, primary_key = True)
    BookID = models.ForeignKey(Book, db_column='BookID',on_delete=models.PROTECT)
    Status = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class BorrowRecord (models.Model):
    BorrowID = models.AutoField(primary_key = True)
    BookInstanceID = models.ForeignKey(BookInstance,db_column='BookInstanceID',on_delete=models.PROTECT)
    Username = models.CharField(max_length=64)
    BorrowDate = models.DateField()
    DueDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name

class Reserve (models.Model):
    ReserveID = models.AutoField(primary_key = True)
    BookID = models.ForeignKey(Book, db_column='BookID', on_delete=models.PROTECT)
    BookInstanceID = models.ForeignKey(BookInstance, db_column='BookInstanceID', on_delete=models.PROTECT, blank=True, null=True)
    Username = models.CharField(max_length=64)
    ReserveDate = models.DateField()
    ReleaseDate = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.name

    def Waiting(self):
        q1 = Q(BookID = self.BookID)
        q2 = Q(ReleaseDate__isnull=True)
        q3 = Q(Username = self.Username)
        y = Reserve.objects.filter(q1 & q2 & q3).values_list()[:1].get()[0]
        q4 = Q(ReserveID__lt = y)
        return Reserve.objects.filter(q1 & q2 & q4).count()+1

# Create your models here.
