from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from django.contrib.sitemaps.views import sitemap
from .models import Project, ProjectPage

# =============================================================================
# PROJECT VIEWS
# =============================================================================

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

    return render(request, 'portfolio/project_page.html', {
        'project': project,
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page
    })

# =============================================================================
# SEO VIEWS
# =============================================================================

@cache_page(60 * 60 * 24 * 7)
def robots_txt(request):
    robots = """
User-agent: *
Allow: /

Sitemap: https://erikwalther.eu/sitemap.xml
    """.strip()
    return HttpResponse(robots, content_type='text/plain')

class StaticSitemap:
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['portfolio:project_list']

    def location(self, item):
        from django.urls import reverse
        return reverse(item)

class ProjectSitemap:
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class ProjectPageSitemap:
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ProjectPage.objects.select_related('project')

    def lastmod(self, obj):
        return obj.updated_at

@cache_page(60 * 60 * 24)
def sitemap_xml_view(request):
    sitemaps = {
        'static': StaticSitemap,
        'projects': ProjectSitemap,
        'project_pages': ProjectPageSitemap,
    }
    return sitemap(request, sitemaps)
