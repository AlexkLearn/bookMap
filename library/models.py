from datetime import timedelta
from django.db import models
from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser


# Create your models here.
ROLE_CHOICES = (
    ("admin", "Admin"),
    ("librarian", "Librarian")
)

class Librarian(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="librarian")
    
    def __str__( self ):
        return f"Username: {self.username} | Role: {self.role}"
    


class Book(models.Model):
    book_cover = models.ImageField(upload_to='book_covers', null=True, blank=True)
    title = models.CharField(max_length=50)
    author = models.TextField(max_length=50)
    
    CATEGORY_CHOICES = (
        ("educational", "Educational"),
        ("informative", "Informative"),
        ("fiction", "Fiction")
    )
    
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES)
    genre = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)
    section = models.CharField(max_length=5)
    shelf = models.CharField(max_length=5)
    row = models.PositiveIntegerField()
    
    @property
    def available_copies ( self ):
        borrowed_count = BorrowedBook.objects.filter( book=self ).count()
        damaged_count = DamagedBook.objects.filter( book=self ).count()
        return self.copies - borrowed_count - damaged_count
    
    def __str__( self ):
        return f"Title: {self.title} | Author: {self.author}"



class BorrowedBook(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrower_name = models.TextField(max_length=50)
    duration = models.DurationField(default=timedelta(days=7))
    
    borrowed_at = models.DateTimeField(default=now)
    
    @property
    def due_date( self ):
        return self.borrowed_at + self.duration
    
    @property
    def status( self ):
        if now() > self.due_date:
            return 'Overdue'
        return 'Active'
    
    
    def __str__(self):
        return f"Title: {self.book.title} | Borrowed_by: {self.borrower_name}"



class DamagedBook(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    reported_by = models.TextField(max_length=50)
    report_date = models.DateTimeField(default=now)
    
    DAMAGE_TYPE = (
        ("water_damage", "Water damage"),
        ("torn_pages", "Torn pages"),
        ("missing_pages", "Missing pages"),
        ("cover_damage", "Cover damage"),
        ("stains", "Stains"),
        ("other", "Other")
    )
    
    damage_type = models.CharField(max_length=30, choices=DAMAGE_TYPE)
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Book: {self.book.title} | Damage: {self.damage_type}"