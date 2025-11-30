from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer


# ------------------------------------------------
# List all books with filtering, search, ordering
# Anyone can read
# ------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Filtering, Searching, Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    


    # ---- FILTERING ----
    filterset_fields = ['title', 'author', 'publication_year']

    # ---- SEARCH ----
    search_fields = ['title', 'author__name']

    # ---- ORDERING ----
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


# ------------------------------------------------
# Retrieve a single book
# ------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ------------------------------------------------
# Create a book (authenticated users)
# ------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ------------------------------------------------
# Update a book (authenticated users)
# ------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# ------------------------------------------------
# Delete a book (admin/staff only)
# ------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]