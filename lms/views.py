from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponse
from django.utils import timezone
from lms.models import Book, BookInstance, BorrowRecord, Reserve
from django.contrib import messages
from lms.forms import BookModelForm, BookInstanceModelForm
from django.db import transaction
from django.contrib.auth.models import User
import datetime


@csrf_exempt
def search_result(request):
    if request.method == 'POST':
        search_text = request.POST['search']
        q1 = Q(BookID__icontains=search_text)
        q2 = Q(Author__icontains=search_text)
        q3 = Q(Title__icontains=search_text)
        q4 = Q(Publisher__icontains=search_text)
        book_list = Book.objects.filter(q1 | q2 | q3 | q4)
        return render(request, 'lms/search_result.html', {'book_list': book_list})


def search_result_details(request):
    if request.method == 'POST':
        book_selected = request.POST['BookID']
        book_list = Book.objects.get(BookID=book_selected)
        bookinstance_list = BookInstance.objects.filter(BookID=book_selected).values('BookInstanceID', 'BookID',
                                                                                     'Status', 'BookID__Title',
                                                                                     'BookID__Author',
                                                                                     'BookID__Publisher')
        context = {
            'book_list': book_list,
            'bookinstance_list': bookinstance_list,
        }
        return render(request, 'lms/search_result_details.html', context)


def borrow(request):
    book_limit = 25
    borrow_day = 30
    if request.method == 'POST':
        book_selected = request.POST['BookID']
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=borrow_day)
        q1 = Q(BookID=book_selected)
        q2 = Q(Status='Available')
        q3 = Q(id=request.user.id)
        q4 = Q(ReturnDate__isnull=True)
        q5 = Q(ReleaseDate__isnull=True)
        q6 = Q(DueDate__lt=now)
        current_borrow = BorrowRecord.objects.filter(q3 & q4).count()
        current_reserve = Reserve.objects.filter(q3 & q5).count()
        if BorrowRecord.objects.filter(q3 & q4 & q6).count() > 0:
            return HttpResponse('u hv overdue book, please return immediately')
        elif current_borrow + current_reserve >= book_limit:
            return HttpResponse('reach total book limit')
        elif BookInstance.objects.filter(q1 & q2).count() > 0:
            x = BookInstance.objects.filter(q1 & q2).values_list()[:1].get()[0]
            FK = BookInstance.objects.get(BookInstanceID=x)
            BookInstance.objects.filter(BookInstanceID=x).update(Status='On Loan')
            BorrowRecord.objects.create(
                BookInstanceID=FK,
                id=request.user,
                BorrowDate=now,
                DueDate=now + delta,
            )
            return HttpResponse('borrow success')
        elif Reserve.objects.filter(q1 & q3 & q5).count() > 0:
            return HttpResponse('u hv reserved this book')
        else:
            FK = Book.objects.get(BookID=book_selected)
            Reserve.objects.create(
                BookID=FK,
                id=request.user,
                ReserveDate=now,
            )
            return HttpResponse('u r in waiting list now')


def book_mgt(request):
    if request.method == 'POST':
        search_text = request.POST['search']
        q1 = Q(BookID__icontains=search_text)
        q2 = Q(Publisher__icontains=search_text)
        q3 = Q(Title__icontains=search_text)
        q4 = Q(Author__icontains=search_text)
        book_list = Book.objects.filter(q1 | q2 | q3 | q4)
    else:
        book_list = Book.objects.all()
    return render(request, 'lms/book_mgt.html', {'book_list': book_list})


def book_edit(request):
    if request.method == 'POST':
        book_selected = request.POST['BookID']
        q1 = Q(BookID__iexact=book_selected)
        item = Book.objects.get(q1)
        if request.POST['action'] == "view":
            form = BookModelForm(instance=item)
            context = {
                'form': form, 'BookID': book_selected}
            return render(request, 'lms/book_edit.html', context)
        elif request.POST['action'] == "submit":
            form = BookModelForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
            book_list = Book.objects.all()
            return render(request, 'lms/book_mgt.html', {'book_list': book_list})


def book_new(request):
    if request.method == 'POST':
        if request.POST['action'] == "view":
            form = BookModelForm()
            context = {
                'form': form}
            return render(request, 'lms/book_new.html', context)
        elif request.POST['action'] == "submit":
            if Book.objects.filter(BookID__iexact=request.POST['BookID']).count() > 0:
                return HttpResponse('The BookID is already exists.')
            elif Book.objects.filter(ISBN__iexact=request.POST['ISBN']).count() > 0:
                return HttpResponse('The ISBN is already exists.')
            elif int(request.POST['number']) > 99:
                return HttpResponse('Total number of books cannot be larger than 99.')
            else:
                form = BookModelForm(request.POST)
                number = request.POST['number']
                if form.is_valid():
                    f = form.save(commit=False)
                    f.BookID = f.BookID.upper()
                    book_selected = f.BookID
                    f.save()
                    FK = Book.objects.get(BookID=book_selected)
                    for i in range(int(number)):
                        x = str(i + 1).zfill(2)
                        BookInstance.objects.create(
                            BookID=FK,
                            Status='Available',
                            BookInstanceID=book_selected + "." + x
                        )
                    book_list = Book.objects.all()
                    return render(request, 'lms/book_mgt.html', {'book_list': book_list})


def bookinstance_mgt(request):
    if request.method == 'POST':
        book_selected = request.POST['BookID']
        book_list = Book.objects.get(BookID=book_selected)
        bookinstance_list = BookInstance.objects.filter(BookID=book_selected)
        context = {
            'book_list': book_list,
            'bookinstance_list': bookinstance_list,
        }
        return render(request, 'lms/bookinstance_mgt.html', context)


def bookinstance_edit(request):
    if request.method == 'POST':
        if request.POST['action'] == "add":
            number = request.POST["number"]
            book_selected = request.POST["BookID"]
            number_exist = BookInstance.objects.filter(BookID=book_selected).count()
            if number_exist + int(number) > 99:
                return HttpResponse('Total number of books cannot be larger than 99.')
            else:
                FK = Book.objects.get(BookID=book_selected)
                for i in range(int(number)):
                    x = str(i + 1 + number_exist).zfill(2)
                    BookInstance.objects.create(
                        BookID=FK,
                        Status='Available',
                        BookInstanceID=book_selected + "." + x
                    )
                book_list = Book.objects.get(BookID=book_selected)
                bookinstance_list = BookInstance.objects.filter(BookID=book_selected)
                context = {
                    'book_list': book_list,
                    'bookinstance_list': bookinstance_list,
                }
                return render(request, 'lms/bookinstance_mgt.html', context)
        else:
            BookInstanceID = request.POST['BookInstanceID']
            q1 = Q(BookInstanceID=BookInstanceID)
            selected = BookInstance.objects.get(q1)
            if request.POST['action'] == "view":
                form = BookInstanceModelForm(instance=selected)
                context = {
                    'form': form,
                    'BookInstanceID': BookInstanceID}
                return render(request, 'lms/bookinstance_edit.html', context)
            elif request.POST['action'] == "submit":
                form = BookInstanceModelForm(request.POST, instance=selected)
                book_selected = request.POST['BookID']
                if form.is_valid():
                    form.save()
                    bookinstance_list = BookInstance.objects.filter(BookID=book_selected)
                    book_list = Book.objects.get(BookID=book_selected)
                    context = {
                        'book_list': book_list,
                        'bookinstance_list': bookinstance_list,
                    }
                    return render(request, 'lms/bookinstance_mgt.html', context)


def check_in(request):
    book_scanned_list = ''
    bookinstance_list = ''
    if request.method == 'POST':
        if request.POST['action'] == "add":
            book_id_scan = request.POST['book_id_scan']
            book_id_scan = book_id_scan.upper()
            book_scanned_list = request.POST['book_scanned_list']
            book_scanned_list = book_scanned_list + "," + book_id_scan
            book_id_selected = book_scanned_list.split(",")
            book_id_selected = list(dict.fromkeys(book_id_selected))
            book_scanned_list = ','.join(book_id_selected)
            bookinstance_list = BookInstance.objects.filter(BookInstanceID__in=book_id_selected).exclude(
                Status__in=['Available', 'Maintenance'])

        elif request.POST['action'] == "del":
            book_id_del = request.POST['book_id_del']
            book_scanned_list = request.POST['book_scanned_list']
            book_id_selected = book_scanned_list.split(",")
            book_id_selected.remove(book_id_del)
            book_id_selected = list(dict.fromkeys(book_id_selected))
            book_scanned_list = ','.join(book_id_selected)
            bookinstance_list = BookInstance.objects.filter(BookInstanceID__in=book_id_selected).exclude(
                Status__in=['Available', 'Maintenance'])

    context = {'book_scanned_list': book_scanned_list, 'bookinstance_list': bookinstance_list}
    return render(request, 'lms/check_in.html', context)


def maintenance(request):
    borrow_day = 30
    if request.method == 'POST':
        if request.POST['action'] == "check_in":
            book_scanned_list = request.POST['book_scanned_list']
            book_id_selected = book_scanned_list.split(",")
            book_id_selected = list(dict.fromkeys(book_id_selected))
            q1 = Q(BookInstanceID__in=book_id_selected)
            q2 = Q(ReturnDate__isnull=True)
            q3 = Q(Status='Maintenance')
            bookinstance_list = BookInstance.objects.filter(q1).exclude(Status__in=['a', 'm'])
            bookinstance_list.update(Status='Maintenance')
            bookinstance_list = BookInstance.objects.filter(q1 & q3)
            BorrowRecord.objects.filter(q1 & q2).values('ReturnDate').update(ReturnDate=datetime.datetime.now())
            check = True
            context = {'bookinstance_list': bookinstance_list, 'check': check}
            return render(request, 'lms/maintenance.html', context)

        elif request.POST['action'] == "release":
            book_checked = request.POST['book_checked']
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=borrow_day)
            book_id_selected = book_checked.split(",")
            book_id_selected = list(dict.fromkeys(book_id_selected))
            if len(book_id_selected) > 0:
                q1 = Q(ReleaseDate__isnull=True)
                for i in range(len(book_id_selected)):
                    bk = book_id_selected[i]
                    q2 = Q(BookID=bk[:-3])
                    q3 = Q(BookInstanceID=bk)
                    if Reserve.objects.filter(q1 & q2).count() > 0:
                        FK = BookInstance.objects.get(q3)
                        y = Reserve.objects.filter(q1 & q2).values_list()[:1].get()[0]
                        user = Reserve.objects.filter(q1 & q2).values_list()[:1].get()[3]
                        Reserve.objects.filter(ReserveID=y).update(
                            ReleaseDate=now,
                            BookInstanceID=FK,
                        )
                        BorrowRecord.objects.create(
                            BookInstanceID=FK,
                            id=user,
                            BorrowDate=now,
                            DueDate=now + delta,
                        )
                        BookInstance.objects.filter(q3).update(
                            Status="On Loan"
                        )
                    else:
                        BookInstance.objects.filter(q3).update(
                            Status="Available"
                        )
            return render(request, 'lms/index.html')
    else:
        bookinstance_list = BookInstance.objects.filter(Status='Maintenance')
        context = {'bookinstance_list': bookinstance_list}
        return render(request, 'lms/maintenance.html', context)


def index(request):
    return render(request, 'lms/index.html')


def record(request):
    q1 = Q(id=request.user.id)
    q2 = Q(ReleaseDate__isnull = True)
    reserve_list = Reserve.objects.filter(q1 & q2)
    borrow_list = BorrowRecord.objects.filter(q1)
    context = {
        'reserve_list':reserve_list,
        'borrow_list':borrow_list,
    }
    return render(request, 'lms/record.html', context)
# Create your views here.
