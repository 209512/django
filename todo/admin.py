from django.contrib import admin
from todo.models import Todo, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('message', 'user')

@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ('id', 'user', 'title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    list_display_links = ('title',)
    summernote_fields = ('description',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_completed', 'completed_image')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'user', 'message', 'created_at')
    list_filter = ('todo', 'user')
    search_fields = ('message', 'user')
    ordering = ('-created_at',)
    list_display_links = ('message',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'user', 'message')
        }),
    )
