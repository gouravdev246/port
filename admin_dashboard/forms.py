from django import forms
from main.models import Project, About, HomePage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'github_link', 'project_link', 'featured', 'image']

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'content', 'profile_image', 'tech_stack']

class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = ['name', 'role', 'tagline', 'background_image', 'is_active']