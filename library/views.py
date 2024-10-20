from django.shortcuts import render
from .models import Book, BookInstance, Genre  # Make sure to import the necessary models

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

# New adding
def index(request):
    num_books = Book.objects.count()  # Count the number of books
    num_books_copied = BookInstance.objects.count()  # Count the number of book instances
    num_genres = Genre.objects.count()  # Count the number of genres
    num_books_available = BookInstance.objects.filter(status__exact='a').count()  # Corrected filter to use 'status'

    payload = {
        'num_books': num_books,  # Total number of books
        'num_books_copied': num_books_copied,  # Total number of book instances
        'num_genres': num_genres,  # Total number of genres
        'num_books_available': num_books_available  # Corrected variable name
    }
    
    return render(request, 'index.html', context=payload)  # Use the payload as context

def base_generic(request):
    return render(request, 'base_generic.html')
