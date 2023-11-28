from django.urls import path
from library import views

urlpatterns = [
    path('', views.home, name='libraryhome'),
    path('uploadfile/', views.bookupload, name='newBook'),
    path('addcategory/', views.addcategory, name='newcategory'),
    path('sales/', views.checkmytotalsales, name='info'),
    path('mybooks/', views.mybooks, name='mybook'),
    path('forsale/<str:title>', views.checkbooksales, name='bookinfosale'),
    path('cpurchase/<str:customer>', views.checkcustomerpurches, name='customerpurchase'),
    path('editfile/<int:pk>', views.edit_book, name='editbook'),
    path('description/<str:description>', views.book_description, name='describebook'),
    path('available/<str:pk>', views.mainbookinformation, name='MainbookDescription'),
    path('buy/<str:pk>', views.buybook, name='buybook'),
    path('searchbyct/<str:ctname>/', views.searchwithcategory, name='searchbycategoty'),
    path('delete/<int:pk>', views.deletebook, name='deletebook'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
 ]
