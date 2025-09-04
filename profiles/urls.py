from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Profile endpoints
    path('profiles/', views.ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/summary/', views.ProfileSummaryView.as_view(), name='profile-summary'),
    
    # Education endpoints
    path('education/', views.EducationListCreateView.as_view(), name='education-list-create'),
    path('education/<int:pk>/', views.EducationDetailView.as_view(), name='education-detail'),
    
    # Skills endpoints
    path('skills/', views.SkillListCreateView.as_view(), name='skill-list-create'),
    path('skills/<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),
    path('skills/top/', views.TopSkillsView.as_view(), name='top-skills'),
    
    # Projects endpoints
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/by-skill/', views.ProjectsBySkillView.as_view(), name='projects-by-skill'),
    
    # Work Experience endpoints
    path('work-experience/', views.WorkExperienceListCreateView.as_view(), name='work-experience-list-create'),
    path('work-experience/<int:pk>/', views.WorkExperienceDetailView.as_view(), name='work-experience-detail'),
    
    # Social Links endpoints
    path('social-links/', views.SocialLinkListCreateView.as_view(), name='social-link-list-create'),
    path('social-links/<int:pk>/', views.SocialLinkDetailView.as_view(), name='social-link-detail'),
    
    # Search endpoint
    path('search/', views.SearchView.as_view(), name='search'),
]
