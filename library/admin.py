from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin import SimpleListFilter
from .models import Librarian, Book, DamagedBook, BorrowedBook


# Customizing the Admin page to display the models columns
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role')
    search_fields = ('username', 'role')
    list_filter = ('role',)
    ordering = ('username',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'genre', 'copies',
        'available_copies', 'section', 'shelf',
        'row'
    )
    
    search_fields = ('title', 'author')
    list_filter = ('category',)
    ordering = ('title',)



# get borrowed book status
class StatusFilter(SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('overdue', 'Overdue'),
        )

    def queryset(self, request, queryset):
        from django.utils.timezone import now
        if self.value() == 'active':
            return queryset.filter(borrowed_at__gte=now() - models.F('duration'))
        if self.value() == 'overdue':
            return queryset.filter(borrowed_at__lt=now() - models.F('duration'))
        return queryset

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_category', 'borrower_name', 'borrowed_at', 'due_date', 'status')
    search_fields = ('book__title', 'borrower_name')
    list_filter = ('book__category', StatusFilter)
    ordering = ('borrowed_at',)

    # Related fields → custom methods
    def get_title(self, obj):
        return obj.book.title
    get_title.short_description = 'Title'

    def get_category(self, obj):
        return obj.book.category
    get_category.short_description = 'Category'



@admin.register(DamagedBook)
class DamagedBookAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'get_category', 'get_genre', 'reported_by', 'damage_type', 'description', 'report_date')
    list_editable = ('damage_type', 'description')
    search_fields = ('book__title', 'damage_type')
    list_filter = ('damage_type', 'book__category')
    ordering = ('report_date',)

    def get_title(self, obj):
        return obj.book.title
    get_title.short_description = 'Title'

    def get_category(self, obj):
        return obj.book.category
    get_category.short_description = 'Category'

    def get_genre(self, obj):
        return obj.book.genre
    get_genre.short_description = 'Genre'