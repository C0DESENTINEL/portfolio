from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('.well-known/security.txt', views.security_txt, name='security_txt'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml_view, name='sitemap_xml'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('<slug:project_slug>/', views.project_detail, name='project_detail'),
    path('<slug:project_slug>/<slug:page_slug>/', views.project_page, name='project_page'),
]
