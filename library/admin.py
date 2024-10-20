from django.contrib import admin
# This code is used to register all our models to the admin site; Django will generate the admin dashboard automatically.
# Register your models here.
from .models import Genre, Book, BookInstance, Language, Author

class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'isbn', 'display_genre']
    ordering = ['id']  # Orders the list by ID in increasing order. Use '-id' to order in decreasing order.

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uniqueid', 'book', 'imprint', 'due_back', 'status']
    ordering = ['due_back']  # Orders by due date
    list_filter = ('status', 'due_back')


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)  # Registering the BookInstance model
admin.site.register(Language)
admin.site.register(Author)


