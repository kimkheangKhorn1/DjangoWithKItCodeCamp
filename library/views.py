from django.shortcuts import render, get_object_or_404
from .models import (
    Book,
    BookInstance,
    Genre,
    Author,
    Language,
)  # Ensure all necessary models are imported

from django.views import generic


# New adding
def index(request):
    num_books = Book.objects.count()  # Count the number of books
    num_books_copied = (
        BookInstance.objects.count()
    )  # Count the number of book instances
    num_genres = Genre.objects.count()  # Count the number of genres
    num_books_available = BookInstance.objects.filter(
        status__exact="a"
    ).count()  # filter to use 'status'

    payload = {
        "num_books": num_books,  # Total number of books
        "num_books_copied": num_books_copied,  # Total number of book instances
        "num_genres": num_genres,  # Total number of genres
        "num_books_available": num_books_available,  # Total number of books available in the library
    }

    return render(request, "index.html", context=payload)  # Use the payload as context


def base_generic(request):
    return render(request, "base_generic.html")


# Ensure you create the book_detail view if you plan to use it.
def book_detail(request):
    return render(request, "book_detail.html")  # Placeholder for book_detail view


# New Adding to views.py
# List of all book
class BookListView(generic.ListView):
    model = Book
    template_name = "book_list.html"  # Specify the template explicitly
    context_object_name = "book_list"  # Match this with the template variable
    queryset = Book.objects.order_by("id")  # Order by ascending ID

    def get_queryset(self):
        # Fetch the books and prefetch the genres for better performance
        return Book.objects.prefetch_related("genre").order_by(
            "id"
        )  # Order by ID in ascending order


# Book Detail
class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"


# List of all authors
class AuthorListView(generic.ListView):
    model = Author
    template_name = "author_list.html"  # Ensure the correct path
    context_object_name = "author_list"

    def get_queryset(self):
        return Author.objects.all().order_by("id")


# Author detail view
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"

    def get_queryset(self):
        # Prefetch related books using the 'books' field
        return Author.objects.prefetch_related("books").all()


# List of all genres
class GenreListView(generic.ListView):
    model = Genre
    template_name = "genre_list.html"  # Specify your template for listing genres
    context_object_name = "genre_list"  # Context variable for the template

    def get_queryset(self):
        return Genre.objects.all().order_by("name")  # Order genres by name


# List of all languages
class LanguageListView(generic.ListView):
    model = Language
    template_name = "language_list.html"  # Specify your template for listing languages
    context_object_name = "language_list"  # Context variable for the template

    def get_queryset(self):
        return Language.objects.all().order_by("name")  # Order languages by name
