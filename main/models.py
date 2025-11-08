from django.db import models
from cloudinary.models import CloudinaryField


class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    profile_image = CloudinaryField('image', blank=True, null=True)
    tech_stack = models.TextField(help_text="Enter tech stack as comma-separated values")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.title

    def get_tech_stack_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.TextField(help_text="Enter tech stack as comma-separated values")
    project_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def get_tech_stack_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class HomePage(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    background_image = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Home Page"

    def __str__(self):
        return f"{self.name} - {self.role}"

    def save(self, *args, **kwargs):
        if self.is_active:
            HomePage.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
