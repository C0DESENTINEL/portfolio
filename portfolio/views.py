from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectPage

def project_list(request):
    projects = Project.objects.filter(is_featured=True) | Project.objects.all()
    # Optioneel: filter alleen gepubliceerde projecten als je een status veld toevoegt
    return render(request, 'portfolio/projects.html', {'projects': projects})

def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})

def project_page(request, project_slug, page_slug):
    project = get_object_or_404(Project, slug=project_slug)
    page = get_object_or_404(ProjectPage, project=project, slug=page_slug)
    
    # Bereken vorige/volgende pagina voor navigatie
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
