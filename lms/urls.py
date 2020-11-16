from django.urls import path

from lms import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_result/', views.search_result, name='search_result'),
    path('borrow/', views.borrow, name='borrow'),
    path('check_in/', views.check_in, name='check_in'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('search_result_details/', views.search_result_details, name='search_result_details'),
    path('bookinstance_mgt/', views.bookinstance_mgt, name='bookinstance_mgt'),
    path('bookinstance_edit/', views.bookinstance_edit, name='bookinstance_edit'),
    path('book_mgt/', views.book_mgt, name='book_mgt'),
    path('book_new/', views.book_new, name='book_new'),
    path('book_edit/', views.book_edit, name='book_edit'),
    path('record/', views.record, name='record'),
]
