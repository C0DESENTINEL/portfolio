from django.contrib import admin
from .models import Project, ProjectPage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_featured')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Algemeen', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Media & Links', {
            'fields': ('featured_image', 'github_url', 'live_url')
        }),
        ('Tags & Featured', {
            'fields': ('tags', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProjectPage)
class ProjectPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'order', 'updated_at')
    list_filter = ('project',)
    search_fields = ('title', 'content_markdown')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('content_html', 'created_at', 'updated_at')

    fieldsets = (
        ('Algemeen', {
            'fields': ('project', 'title', 'slug', 'order')
        }),
        ('Content', {
            'fields': ('content_markdown', 'content_html')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
