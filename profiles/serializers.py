from rest_framework import serializers
from .models import (
    Profile, Education, Skill, Project, ProjectLink, 
    ProjectSkill, WorkExperience, SocialLink
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = '__all__'


class ProjectSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_level = serializers.CharField(source='skill.level', read_only=True)
    
    class Meta:
        model = ProjectSkill
        fields = ['id', 'skill', 'skill_name', 'skill_level']


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    links = ProjectLinkSerializer(many=True, read_only=True)
    project_skills = ProjectSkillSerializer(many=True, read_only=True)
    skills = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_skills(self, obj):
        return [ps.skill.name for ps in obj.project_skills.all()]


class ProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    work_experience = WorkExperienceSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for profile summaries"""
    skills_count = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'bio', 'skills_count', 'projects_count']
    
    def get_skills_count(self, obj):
        return obj.skills.count()
    
    def get_projects_count(self, obj):
        return obj.projects.count()


class SkillSummarySerializer(serializers.ModelSerializer):
    """Serializer for skill statistics"""
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'level', 'years_experience', 'projects_count']
    
    def get_projects_count(self, obj):
        return obj.projectskill_set.count()


class ProjectSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for project listings"""
    skills = serializers.SerializerMethodField()
    links_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 
                 'is_ongoing', 'skills', 'links_count']
    
    def get_skills(self, obj):
        return [ps.skill.name for ps in obj.project_skills.all()]
    
    def get_links_count(self, obj):
        return obj.links.count()
