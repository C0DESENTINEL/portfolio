# portfolio/models.py
from django.db import models
from django.utils.text import slugify
import markdown
import nh3

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titel")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Korte beschrijving")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Featured afbeelding")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    live_url = models.URLField(blank=True, verbose_name="Live URL")
    tags = models.JSONField(default=list, blank=True, verbose_name="Tags")
    is_featured = models.BooleanField(default=False, verbose_name="Uitgelicht?")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projecten"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectPage(models.Model):
    project = models.ForeignKey(Project, related_name='pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Pagina Titel")
    slug = models.SlugField(verbose_name="Pagina Slug")
    # Verwijder EasyMDEField en gebruik standaard TextField
    content_markdown = models.TextField(help_text="Schrijf hier je content in Markdown", verbose_name="Content (Markdown)")
    content_html = models.TextField(editable=False, verbose_name="Content (HTML)")
    order = models.IntegerField(default=0, verbose_name="Volgorde")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['project', 'slug']
        verbose_name = "Project Pagina"
        verbose_name_plural = "Project Pagina's"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        md = markdown.markdown(
            self.content_markdown,
            extensions=['fenced_code', 'codehilite', 'toc', 'tables', 'nl2br']
        )

        allowed_tags = {
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'img', 'hr',
            'table', 'thead', 'tbody', 'tr', 'th', 'td'
        }
        allowed_attrs = {
            '*': {'class', 'id'},
            'a': {'href', 'title', 'target'},
            'img': {'src', 'alt', 'title'}
        }

        self.content_html = nh3.clean(md, tags=allowed_tags, attributes=allowed_attrs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} - {self.title}"
