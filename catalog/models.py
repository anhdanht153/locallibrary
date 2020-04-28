from django.db import models
from django.urls import reverse
import uuid                         # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    """書籍の種類のモデル""" 
    name = models.CharField(max_length=200, help_text="Enter a book genre") 

    def __str__(self):
        """モデルオブジェクトを表すための文字列""" 
        return self.name

class Book(models.Model):
    """書籍オブジェクトを表す""" 
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length= 1000, help_text="Enter a brief description of the book")
    isbn = models.CharField("ISBN", max_length=13, help_text='13 Character <a href = "https://www.isbn.international.org/content/what-isbn"> ISBN number </a>')
    genre = models.ManyToManyField("Genre", help_text="Select a genre for this book")

    def __str__(self):
        """モデルオブジェクトを表すための文字列""" 
        return self.title

    def get_absolute_url(self):
        """URLを戻す""" 
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin.""" 
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Book Instanceを表す""" 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Uniquy ID for this paticular book across whole libary")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintainance"),
        ("o", "On Loan"),
        ("a", "Available"),
        ("r", "Reversed"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """モデルオブジェクトを表すための文字列""" 
        return f'({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        
class Author(models.Model):
    """作者を表す""" 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """URLを戻す""" 
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        """モデルオブジェクトを表すための文字列""" 
        return f'{self.last_name}, {self.first_name}'
