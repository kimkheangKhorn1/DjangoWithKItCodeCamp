from django.urls import path
from . import views


urlpatterns = [
    # New Adding
    path('', views.index, name='index'),
    path('base_generic/', views.base_generic, name='base_generic'),
    path('book_detail/', views.book_detail, name='book_detail'),  # Updated URL for book_detail
    path('books/', views.BookListView.as_view(), name='books'),  # List of all books
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'), # Detail for each book
    
     # New URLs for authors, genres, and languages
    path('authors/', views.AuthorListView.as_view(), name='authors'),  # List view for all authors
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),  # Detail view for each author
    path('genres/', views.GenreListView.as_view(), name='genres'),  # List of all genres
    path('languages/', views.LanguageListView.as_view(), name='languages'),  # List of all languages
        
]
