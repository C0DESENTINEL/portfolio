# portfolio/models.py
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import markdown
import nh3
import json
import os

# Definieer de beschikbare afbeeldingen (pas deze lijst aan naar gelang je bestanden)
FEATURED_IMAGE_CHOICES = [
    ('', '— Geen afbeelding —'),
    ('images/tor-relay.svg', 'Tor Relay'),
    ('images/hack-the-box.svg', 'Hack The Box'),
    ('images/boot-dev.svg', 'Boot.dev'),
    ('images/portfolio.svg', 'Portfolio Site'),
    # Voeg hier nieuwe bestanden toe als je ze in static/images/ zet
]

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description (Markdown)")
    description_html = models.TextField(editable=False, verbose_name="Description (HTML)", default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    featured_image = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=FEATURED_IMAGE_CHOICES,
        default='',
        verbose_name="Featured image",
        help_text="Choose an image from the list (path is relative to static/images/)."
    )

    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    live_url = models.URLField(blank=True, verbose_name="Live URL")
    tags = models.JSONField(default=list, blank=True, verbose_name="Tags")
    is_featured = models.BooleanField(default=False, verbose_name="Featured?")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projecten"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.description:
            md = markdown.markdown(
                self.description,
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
            self.description_html = nh3.clean(md, tags=allowed_tags, attributes=allowed_attrs)
        else:
            self.description_html = ""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def _detect_category(self):
        title_lower = self.title.lower()
        tags_lower = [t.lower() for t in self.tags] if isinstance(self.tags, list) else []

        if 'hack the box' in title_lower or 'boot.dev' in title_lower or 'certification' in title_lower:
            return 'study'
        if 'tor' in title_lower or 'relay' in title_lower or 'network' in title_lower or 'privacypal' in title_lower:
            return 'infrastructure'
        if 'django' in title_lower or 'portfolio' in title_lower or self.github_url:
            return 'software'
        return 'other'

    def get_schema_type(self):
        category = self._detect_category()
        mapping = {
            'study': 'LearningResource',
            'infrastructure': 'WebApplication',
            'software': 'WebApplication',
            'other': 'SoftwareSourceCode'
        }
        return mapping.get(category, 'SoftwareSourceCode')

    def get_schema_data(self):
        category = self._detect_category()

        base_data = {
            "@context": "https://schema.org",
            "@type": self.get_schema_type(),
            "name": self.title,
            "description": self.description,
            "author": {
                "@type": "Person",
                "name": "Erik Walther",
                "url": "https://erikwalther.eu"
            },
            "datePublished": self.created_at.strftime('%Y-%m-%d'),
            "dateModified": self.updated_at.strftime('%Y-%m-%d'),
        }

        if category == 'study':
            provider_name = "Hack The Box" if "Hack The Box" in self.title else "Boot.dev"
            provider_url = "https://www.hackthebox.com" if "Hack The Box" in self.title else "https://www.boot.dev"
            base_data.update({
                "provider": { "@type": "Organization", "name": provider_name, "url": provider_url },
                "educationalLevel": "Intermediate",
                "learningResourceType": "Certification"
            })
        elif category == 'infrastructure':
            base_data.update({ "applicationCategory": "NetworkApplication", "operatingSystem": "Linux" })
        elif category == 'software':
            base_data.update({ "applicationCategory": "Web Application", "operatingSystem": "Linux", "softwareVersion": "1.0" })

        if self.live_url:
            base_data["url"] = self.live_url

        if self.featured_image:
            base_data["image"] = {
                "@type": "ImageObject",
                "url": f"https://erikwalther.eu/static/{self.featured_image}",
                "caption": f"{self.title} featured image"
            }

        return base_data

    def get_schema_json(self):
        return json.dumps(self.get_schema_data(), ensure_ascii=False)

class ProjectPage(models.Model):
    project = models.ForeignKey(Project, related_name='pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Pagina Titel")
    slug = models.SlugField(verbose_name="Pagina Slug")
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
        md = markdown.markdown(self.content_markdown, extensions=['fenced_code', 'codehilite', 'toc', 'tables', 'nl2br'])
        allowed_tags = {'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'img', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td'}
        allowed_attrs = {'*': {'class', 'id'}, 'a': {'href', 'title', 'target'}, 'img': {'src', 'alt', 'title'}}
        self.content_html = nh3.clean(md, tags=allowed_tags, attributes=allowed_attrs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} - {self.title}"
