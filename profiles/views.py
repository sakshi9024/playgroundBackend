from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Profile, Education, Skill, Project, ProjectLink,
    ProjectSkill, WorkExperience, SocialLink
)
from .serializers import (
    ProfileSerializer, ProfileSummarySerializer, EducationSerializer,
    SkillSerializer, SkillSummarySerializer, ProjectSerializer,
    ProjectSummarySerializer, WorkExperienceSerializer, SocialLinkSerializer
)


# Health check endpoint
@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Profile API is running',
        'timestamp': timezone.now()
    })


# Profile CRUD endpoints
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Education CRUD endpoints
class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


# Skills CRUD endpoints
class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


# Projects CRUD endpoints
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


# Work Experience CRUD endpoints
class WorkExperienceListCreateView(generics.ListCreateAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


# Social Links CRUD endpoints
class SocialLinkListCreateView(generics.ListCreateAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class SocialLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


# Specialized Query Endpoints
class ProjectsBySkillView(APIView):
    """GET /projects?skill=python - Filter projects by skill"""

    def get(self, request):
        skill_name = request.query_params.get('skill')
        if not skill_name:
            return Response({'error': 'skill parameter is required'},
                          status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(
            project_skills__skill__name__icontains=skill_name
        ).distinct()

        serializer = ProjectSummarySerializer(projects, many=True)
        return Response({
            'skill': skill_name,
            'count': projects.count(),
            'projects': serializer.data
        })


class TopSkillsView(APIView):
    """GET /skills/top - Get top skills by usage in projects"""

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))

        skills = Skill.objects.annotate(
            project_count=Count('projectskill')
        ).order_by('-project_count', '-years_experience')[:limit]

        serializer = SkillSummarySerializer(skills, many=True)
        return Response({
            'count': skills.count(),
            'skills': serializer.data
        })


class SearchView(APIView):
    """GET /search?q=... - Search across projects, skills, and work experience"""

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'error': 'q parameter is required'},
                          status=status.HTTP_400_BAD_REQUEST)

        # Search projects
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

        # Search skills
        skills = Skill.objects.filter(
            name__icontains=query
        ).distinct()

        # Search work experience
        work_experience = WorkExperience.objects.filter(
            Q(company__icontains=query) |
            Q(position__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

        return Response({
            'query': query,
            'results': {
                'projects': {
                    'count': projects.count(),
                    'data': ProjectSummarySerializer(projects, many=True).data
                },
                'skills': {
                    'count': skills.count(),
                    'data': SkillSummarySerializer(skills, many=True).data
                },
                'work_experience': {
                    'count': work_experience.count(),
                    'data': WorkExperienceSerializer(work_experience, many=True).data
                }
            }
        })


class ProfileSummaryView(APIView):
    """GET /profile/summary - Get profile summary with counts"""

    def get(self, request):
        try:
            profile = Profile.objects.first()  # Get the first profile
            if not profile:
                return Response({'error': 'No profile found'},
                              status=status.HTTP_404_NOT_FOUND)

            serializer = ProfileSummarySerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'},
                          status=status.HTTP_404_NOT_FOUND)
