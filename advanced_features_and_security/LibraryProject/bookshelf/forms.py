# LibraryProject/bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm, BookSearchForm
from .forms import ExampleForm


# Add a new book
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# Search books safely
def search_books(request):
    form = BookSearchForm(request.GET)
    books = []
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/search_results.html', {'form': form, 'books': books})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books.
    Only accessible to users with 'can_view' permission.
    """
    books = Book.objects.all()  # Query all books
    context = {
        'books': books,
        'example_form': ExampleForm()   # ← Optional: include ExampleForm if needed in template
    }
    return render(request, 'bookshelf/book_list.html', context)