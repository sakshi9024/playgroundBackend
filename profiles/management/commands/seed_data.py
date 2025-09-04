from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from profiles.models import (
    Profile, Education, Skill, Project, ProjectLink, 
    ProjectSkill, WorkExperience, SocialLink
)


class Command(BaseCommand):
    help = 'Seed the database with sample profile data'

    def handle(self, *args, **options):
        # Clear existing data
        Profile.objects.all().delete()
        
        # Create profile
        profile = Profile.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            bio="Full-stack developer with 5+ years of experience in web development, "
                "specializing in Python, Django, React, and cloud technologies. "
                "Passionate about building scalable applications and learning new technologies."
        )
        
        # Create education
        Education.objects.create(
            profile=profile,
            institution="University of Technology",
            degree="Bachelor of Science",
            field_of_study="Computer Science",
            start_date=date(2018, 9, 1),
            end_date=date(2022, 6, 30),
            description="Graduated with honors. Focused on software engineering, algorithms, and data structures."
        )
        
        # Create skills
        skills_data = [
            {"name": "Python", "level": "expert", "years_experience": 5},
            {"name": "Django", "level": "expert", "years_experience": 4},
            {"name": "JavaScript", "level": "advanced", "years_experience": 4},
            {"name": "React", "level": "advanced", "years_experience": 3},
            {"name": "PostgreSQL", "level": "advanced", "years_experience": 3},
            {"name": "Docker", "level": "intermediate", "years_experience": 2},
            {"name": "AWS", "level": "intermediate", "years_experience": 2},
            {"name": "Git", "level": "expert", "years_experience": 5},
            {"name": "HTML/CSS", "level": "expert", "years_experience": 5},
            {"name": "Node.js", "level": "intermediate", "years_experience": 2},
        ]
        
        skills = []
        for skill_data in skills_data:
            skill = Skill.objects.create(profile=profile, **skill_data)
            skills.append(skill)
        
        # Create work experience
        WorkExperience.objects.create(
            profile=profile,
            company="Tech Solutions Inc.",
            position="Senior Full Stack Developer",
            location="San Francisco, CA",
            start_date=date(2022, 7, 1),
            is_current=True,
            description="Lead development of web applications using Django and React. "
                       "Mentor junior developers and collaborate with cross-functional teams."
        )
        
        WorkExperience.objects.create(
            profile=profile,
            company="StartupXYZ",
            position="Full Stack Developer",
            location="Remote",
            start_date=date(2021, 1, 15),
            end_date=date(2022, 6, 30),
            description="Developed and maintained multiple web applications. "
                       "Implemented CI/CD pipelines and improved application performance by 40%."
        )
        
        # Create projects
        project1 = Project.objects.create(
            profile=profile,
            title="E-commerce Platform",
            description="A full-featured e-commerce platform built with Django and React. "
                       "Features include user authentication, product catalog, shopping cart, "
                       "payment integration, and admin dashboard.",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 6, 30)
        )
        
        project2 = Project.objects.create(
            profile=profile,
            title="Task Management API",
            description="RESTful API for task management with user authentication, "
                       "project organization, and real-time notifications using WebSockets.",
            start_date=date(2022, 8, 1),
            end_date=date(2022, 12, 31)
        )
        
        project3 = Project.objects.create(
            profile=profile,
            title="Weather Dashboard",
            description="React-based weather dashboard that displays current weather "
                       "and forecasts for multiple cities with interactive charts.",
            start_date=date(2023, 7, 1),
            is_ongoing=True
        )
        
        # Create project links
        ProjectLink.objects.create(
            project=project1,
            url="https://github.com/johndoe/ecommerce-platform",
            link_type="github",
            description="Source code repository"
        )
        
        ProjectLink.objects.create(
            project=project1,
            url="https://ecommerce-demo.example.com",
            link_type="demo",
            description="Live demo"
        )
        
        ProjectLink.objects.create(
            project=project2,
            url="https://github.com/johndoe/task-api",
            link_type="github"
        )
        
        ProjectLink.objects.create(
            project=project3,
            url="https://github.com/johndoe/weather-dashboard",
            link_type="github"
        )
        
        # Create project skills relationships
        # E-commerce platform skills
        for skill_name in ["Python", "Django", "React", "PostgreSQL"]:
            skill = next(s for s in skills if s.name == skill_name)
            ProjectSkill.objects.create(project=project1, skill=skill)
        
        # Task API skills
        for skill_name in ["Python", "Django", "PostgreSQL"]:
            skill = next(s for s in skills if s.name == skill_name)
            ProjectSkill.objects.create(project=project2, skill=skill)
        
        # Weather dashboard skills
        for skill_name in ["JavaScript", "React", "HTML/CSS"]:
            skill = next(s for s in skills if s.name == skill_name)
            ProjectSkill.objects.create(project=project3, skill=skill)
        
        # Create social links
        SocialLink.objects.create(
            profile=profile,
            platform="github",
            url="https://github.com/johndoe",
            description="Personal GitHub profile"
        )
        
        SocialLink.objects.create(
            profile=profile,
            platform="linkedin",
            url="https://linkedin.com/in/johndoe",
            description="Professional LinkedIn profile"
        )
        
        SocialLink.objects.create(
            profile=profile,
            platform="portfolio",
            url="https://johndoe.dev",
            description="Personal portfolio website"
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with profile data')
        )
