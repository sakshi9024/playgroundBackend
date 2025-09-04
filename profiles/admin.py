from django.contrib import admin
from .models import Profile, Education, Skill, Project, ProjectLink, ProjectSkill, WorkExperience, SocialLink


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    inlines = [EducationInline, SkillInline, WorkExperienceInline, SocialLinkInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'profile', 'start_date', 'end_date', 'is_ongoing']
    list_filter = ['is_ongoing', 'start_date']
    search_fields = ['title', 'description']
    inlines = [ProjectLinkInline, ProjectSkillInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'profile', 'start_date', 'end_date']
    list_filter = ['degree', 'start_date']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'years_experience', 'profile']
    list_filter = ['level', 'years_experience']
    search_fields = ['name']


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'profile', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']


admin.register(ProjectLink)
admin.register(ProjectSkill)
admin.register(SocialLink)
