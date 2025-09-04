from django.db import models
from django.core.validators import URLValidator


class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], default='intermediate')
    years_experience = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['profile', 'name']

    def __str__(self):
        return f"{self.name} ({self.level})"


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_ongoing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectLink(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=[
        ('github', 'GitHub'),
        ('demo', 'Live Demo'),
        ('documentation', 'Documentation'),
        ('other', 'Other')
    ])
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.project.title} - {self.link_type}"


class ProjectSkill(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['project', 'skill']

    def __str__(self):
        return f"{self.project.title} - {self.skill.name}"


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.company}"


class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=[
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('portfolio', 'Portfolio'),
        ('twitter', 'Twitter'),
        ('other', 'Other')
    ])
    url = models.URLField()
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ['profile', 'platform']

    def __str__(self):
        return f"{self.profile.name} - {self.platform}"
