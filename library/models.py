import uuid  # Import the UUID module for generating unique IDs
from datetime import date  # Import the date class for date comparisons
from django.conf import settings  # Import Django settings to reference the user model
from django.urls import reverse  # Import the reverse function to resolve URLs
from django.db import models  # Import the models module from Django's ORM
from django.db.models import UniqueConstraint  # Import UniqueConstraint to enforce uniqueness
from django.db.models.functions import Lower  # Import Lower for case-insensitive queries

class Genre(models.Model):
    """
    Represents a genre of books.
    Each genre has a unique name.
    """
    name = models.CharField(
        max_length=200,  # Maximum length for the genre name
        unique=True,  # Ensure no two genres have the same name
        help_text="Enter a Book Genre (e.g., Science, Fantasy, Non-fiction, History...)",  # Help text for the admin
    )

    class Meta:
        # Metadata options for the Genre model
        constraints = [
            UniqueConstraint(  # Ensure uniqueness of the genre name regardless of case
                Lower("name"),  # Apply the constraint to the lowercase version of the name
                name="genre_name_case_insensitive_unique",  # Name for the constraint
                violation_error_message="Genre already exists",  # Message if the constraint fails
            )
        ]

    def __str__(self):
        # String representation of the genre
        return self.name  # Return the genre name

    def get_absolute_url(self):
        # Returns the URL for the genre detail view
        return reverse("genre_detail", args=[str(self.id)])  # Use reverse to get the URL


class Author(models.Model):
    """
    Represents an author of books.
    Each author has a name, date of birth, and date of death.
    """
    name = models.CharField(max_length=100, help_text="Enter the author's name.")  # Author's name
    date_of_birth = models.DateField(null=True, blank=True, help_text="Enter the author's date of birth.")  # Optional date of birth
    date_of_death = models.DateField(null=True, blank=True, help_text="Enter the author's date of death (if applicable).")  # Optional date of death
    books = models.ManyToManyField("Book", help_text="Select books written by this author.")  # Corrected to reference 'Book' instead of 'BookI'

    def __str__(self):
        # String representation of the author
        return self.name  # Return the author's name


class Language(models.Model):
    """
    Represents a language in which books are written.
    Each language can be associated with multiple books.
    """
    name = models.CharField(max_length=100, help_text="Enter the language name.")  # Language name
    books = models.ManyToManyField(
        "Book",  # Corrected to reference 'Book' instead of 'BookI'
        related_name="languages",  # Related name to avoid clashes with other relationships
        help_text="Select books in this language."  # Help text for the admin
    )

    def __str__(self):
        # String representation of the language
        return self.name  # Return the language name


class Book(models.Model):
    """
    Represents a book in the library.
    Each book has a title, summary, ISBN, genre, and language.
    """
    title = models.CharField(max_length=300, help_text="Enter the Book Title.")  # Book title
    summary = models.TextField(max_length=1500, help_text="Enter the Book Description.")  # Summary of the book
    isbn = models.CharField(
        max_length=20,  # Maximum length for ISBN
        unique=True,  # Ensure no two books have the same ISBN
        help_text='20 Characters <a href="https://isbnsearch.org/">ISBN Search</a>.'  # Help text with a link for ISBN search
    )

    genre = models.ManyToManyField(  # Many-to-many relationship with genres
        Genre,  # Reference to the Genre model
        help_text="Select a Genre or Many for the Book."  # Help text for the admin
    )

    language = models.ForeignKey(  # Foreign key to the Language model
        Language,  # Reference to the Language model
        on_delete=models.SET_NULL,  # Set to null if the language is deleted
        null=True,  # Allow null values for this field
        blank=True  # Allow blank values for this field
    )

    class Meta:
        # Metadata options for the Book model
        ordering = ["title"]  # Default ordering by book title

    def get_absolute_url(self):
        # Returns the URL for the book detail view
        return reverse("book_detail", args=[str(self.id)])  # Use reverse to get the URL

    def __str__(self):
        # String representation of the book
        return f'{self.id}. {self.title}' # Return the book title
    
    def display_genre(self):
        list_genres_name = self.genre.all()  # Corrected variable name
        genre_names = []
        for genre in list_genres_name:
            genre_names.append(genre.name)  # Use parentheses to call append and access the genre name
        return ', '.join(genre_names)

    display_genre.short_description = 'Genre'  # Corrected spelling of 'short_description'

class BookInstance(models.Model):
    """
    Represents a specific copy of a book in the library.
    Each instance has a unique ID, imprint, due date, borrower, and status.
    """
    uniqueid = models.UUIDField(
        primary_key=True,  # Set as the primary key
        default=uuid.uuid4,  # Generate a unique ID using UUID4
        help_text="Unique Id for this particular Book Copy in Library"  # Help text for the admin
    )
    
    imprint = models.CharField(max_length=200)  # Book's imprint
    due_back = models.DateField(null=True, blank=True)  # Date when the book is due back
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the user model specified in settings
        on_delete=models.SET_NULL,  # Set to null if the user is deleted
        null=True,  # Allow null values for this field
        blank=True  # Allow blank values for this field
    )

    LOAN_STATUS = (  # Choices for the loan status
        ('m', 'Maintenance'),  # Book is under maintenance
        ('o', 'On Loan'),  # Book is currently on loan
        ('a', 'Available'),  # Book is available for checkout
        ('r', 'Reserved')  # Book is reserved
    )
    
    status = models.CharField(
        max_length=1,  # Maximum length for status
        choices=LOAN_STATUS,  # Set choices for the status
        blank=True,  # Allow the field to be blank
        default='m',  # Default status is maintenance
        help_text='Book Availability'  # Help text for the admin
    )
    
    book = models.ForeignKey(
        Book,  # Reference to the Book model
        on_delete=models.RESTRICT,  # Prevent deletion if there are related instances
        null=True  # Allow null values for this field
    )

    class Meta:
        # Metadata options for the BookInstance model
        ordering = ['due_back', 'imprint']  # Default ordering by due date and imprint

    def __str__(self):
        # String representation of the book instance
        return  f'{self.uniqueid} [{self.book.title}]'  # Return the title of the associated book

    def get_absolute_url(self):
        # Returns the URL for the book instance detail view
        return reverse("bookinstance_detail", args=[str(self.id)])  # Use reverse to get the URL

    @property
    def is_overdue(self):
        # Check if the book instance is overdue
        return bool(self.due_back and date.today() > self.due_back)  # Return True if overdue
