from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q

from .models import Book, BorrowedBook, DamagedBook, Librarian


# User
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # phone = request.POST.get('phone')
        role = request.POST.get('role', 'librarian')

        # Create user safely (password hashed)
        user = Librarian.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            #phone=phone,
            role=role
        )
        
        # Log in user after registering
        login(request, user)

        return redirect("dashboard")

    return render( request, "register.html" )



def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect('home')


def visitor_view(request):
    return render(request, "hello.html")


# Read Book Instances
@login_required
def dashboard(request):
    user = request.user
    books = Book.objects.all()
    borrowed = BorrowedBook.objects.all()
    damaged = DamagedBook.objects.all()

    sort = request.GET.get( "sort", "asc" )  # default asc

    if sort == "asc":
        books = Book.objects.all().order_by( "title" )
    else:
        books = Book.objects.all().order_by( "-title" )

    next_sort = "desc" if sort == "asc" else "asc"

    search_query = request.GET.get( 'search' )
    if search_query:
        books = books.filter(
            Q( title__icontains=search_query ) |
            Q( author__icontains=search_query ) |
            Q( genre__icontains=search_query )
        )
        
    if request.user.role == 'admin':
        initials = user.username[0].upper()
    else:
        initials = f"{user.first_name[0].upper()}{user.last_name[0].upper()}"
     
    context = {
        "user": user,
        "books": books,
        "borrowed": borrowed,
        "damaged": damaged,
        "initials": initials,
        "next_sort": next_sort,
    }
    
    return render(request, 'index.html', context)



def add_book(request):
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        genre = request.POST.get('genre')
        copies = request.POST.get('copies')
        section = request.POST.get('section')
        shelf = request.POST.get('shelf')
        row = request.POST.get('row')
        book_cover = request.FILES.get('cover')
        
        Book.objects.create(
            title=title, author=author, genre=genre,
            category=category, copies=copies, row=row,
            section=section, shelf=shelf, book_cover=book_cover
        )
        return redirect('dashboard')
    
    return render(request, 'add_book.html')


def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    book.delete()
    
    return redirect('dashboard')



def borrow_book(request):
    if request.method == "POST":
        title = request.POST.get( "title" )
        borrower_name = request.POST.get( "borrower" )
        duration_days = request.POST.get( "duration")

        # check book exists
        try:
            book = Book.objects.get( title=title )
        except Book.DoesNotExist:
            messages.error( request, "No such book exists." )
            return redirect( "borrow_book" )

        # check available copies
        if book.available_copies <= 0:
            messages.error( request, "No available copies of this book." )
            return redirect( "borrow_book" )

        # create borrowed book
        BorrowedBook.objects.create(
            book=book,
            borrower_name=borrower_name,
            duration=timedelta( days=int( duration_days ) )
        )
        
        messages.success( request, f"You have borrowed '{book.title}'" )
        return redirect( "dashboard" )
    
    return render(request, 'borrow.html')


def return_book(request, pk):
    borrowed_book = get_object_or_404(BorrowedBook, id=pk)
    borrowed_book.delete()
    
    return redirect('dashboard')


def edit_book( request, pk ):
    book = get_object_or_404( Book, id=pk )
    context = { "book": book }

    if request.method == 'POST':
        book.title = request.POST.get( 'title' )
        book.author = request.POST.get( 'author' )
        book.category = request.POST.get( 'category' )
        book.genre = request.POST.get( 'genre' )
        book.copies = request.POST.get( 'copies' )
        book.section = request.POST.get( 'section' )
        book.shelf = request.POST.get( 'shelf' )
        book.row = request.POST.get( 'row' )

        # check if a new image is uploaded before updating
        if 'cover' in request.FILES:
            book.book_cover = request.FILES.get('cover')

        book.save()

        return redirect('dashboard')
    
    return render(request, 'edit_book.html', context)


def report_damage(request):
    if request.method == "POST":
        title = request.POST.get( "title" )
        reported_by = request.POST.get("reporter")
        damage_type = request.POST.get("damage")
        description = request.POST.get("description")

        # check if such book exists
        try:
            book = Book.objects.get( title=title )
        except Book.DoesNotExist:
            messages.error( request, "No such book exists." )
            return redirect( "report_damage" )

        # save damage record
        DamagedBook.objects.create(
            book=book,
            reported_by=reported_by,
            report_date=now(),
            damage_type=damage_type,
            description=description
        )

        messages.success( request, f"Damage reported for '{book.title}'" )
        return redirect( "dashboard" )

    return render( request, "damaged.html" )