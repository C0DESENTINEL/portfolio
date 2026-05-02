from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import Project, ProjectPage, SiteIntro

def homepage(request):
    intro = SiteIntro.objects.first()

    recent_pages = ProjectPage.objects.select_related('project').order_by('-created_at')[:4]

    return render(request, 'portfolio/homepage.html', {
        'intro': intro,
        'recent_pages': recent_pages,
    })

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': projects})

def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})

def project_page(request, project_slug, page_slug):
    project = get_object_or_404(Project, slug=project_slug)
    page = get_object_or_404(ProjectPage, project=project, slug=page_slug)

    all_pages = list(project.pages.order_by('order'))
    try:
        index = all_pages.index(page)
        previous_page = all_pages[index - 1] if index > 0 else None
        next_page = all_pages[index + 1] if index < len(all_pages) - 1 else None
    except ValueError:
        previous_page = None
        next_page = None

    project_schema_type = project.get_schema_type()

    return render(request, 'portfolio/project_page.html', {
        'project': project,
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'project_schema_type': project_schema_type,
    })

def privacy_policy(request):
    last_updated = timezone.make_aware(
        timezone.datetime(2026, 4, 26, 7, 0, 0)
    )
    return render(request, 'privacy_policy.html', {
        'last_updated': last_updated,
    })

def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['portfolio:homepage', 'portfolio:project_list', 'portfolio:privacy_policy']

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        latest_project = Project.objects.order_by('-updated_at').first()
        return latest_project.updated_at if latest_project else timezone.now()

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse('portfolio:project_detail', kwargs={'project_slug': obj.slug})

    def lastmod(self, obj):
        return obj.updated_at

class ProjectPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return ProjectPage.objects.select_related('project')

    def location(self, obj):
        return reverse('portfolio:project_page', kwargs={
            'project_slug': obj.project.slug,
            'page_slug': obj.slug
        })

    def lastmod(self, obj):
        return obj.updated_at

def sitemap_xml_view(request):
    sitemaps = {
        'static': StaticSitemap(),
        'projects': ProjectSitemap(),
        'project_pages': ProjectPageSitemap(),
    }
    return sitemap(request, sitemaps)
