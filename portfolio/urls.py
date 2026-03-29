from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<slug:project_slug>/', views.project_detail, name='project_detail'),
    path('<slug:project_slug>/<slug:page_slug>/', views.project_page, name='project_page'),
]
