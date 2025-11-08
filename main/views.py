from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HomePage, About, Project, ContactMessage
from .forms import ContactForm


def home(request):
    home_page = HomePage.objects.filter(is_active=True).first()
    featured_projects = Project.objects.filter(featured=True)[:3]
    context = {
        'home_page': home_page,
        'featured_projects': featured_projects,
    }
    return render(request, 'main/home.html', context)


def about(request):
    about_content = About.objects.first()
    context = {
        'about': about_content,
    }
    return render(request, 'main/about.html', context)


def projects(request):
    projects_list = Project.objects.filter(featured=True)[:6]
    all_projects = Project.objects.all()
    context = {
        'featured_projects': projects_list,
        'all_projects': all_projects,
    }
    return render(request, 'main/projects.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'main/contact.html', context)
