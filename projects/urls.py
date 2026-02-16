from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main pages
    path('welcome/', views.welcome_view, name='welcome'),
    
    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.new_project, name='new_project'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:project_id>/history/', views.released_history, name='released_history'),
    
    # Branches
    path('projects/<int:project_id>/branches/new/', views.new_branch, name='new_branch'),
    path('branches/<int:branch_id>/delete/', views.delete_branch, name='delete_branch'),
    path('branches/<int:branch_id>/history/', views.branch_history, name='branch_history'),
    
    # Released History
    path('released/<int:history_id>/edit/', views.edit_released_history, name='edit_released_history'),
    path('released/<int:history_id>/delete/', views.delete_released_history, name='delete_released_history'),
    
    # Sub-Branches
    path('subbranches/<int:subbranch_id>/edit/', views.edit_subbranch, name='edit_subbranch'),
    path('subbranches/<int:subbranch_id>/delete/', views.delete_subbranch, name='delete_subbranch'),
]
