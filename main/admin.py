from django.contrib import admin
from .models import About, Project, ContactMessage, HomePage


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'content']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'display_order', 'created_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured', 'display_order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'created_at']
    list_editable = ['is_active']
