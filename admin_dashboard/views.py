from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import requests
from decouple import config
import logging
from main.models import Project, About, HomePage, ContactMessage
from main.forms import ContactForm

logger = logging.getLogger('login_attempts')

@login_required
def dashboard(request):
    """Main admin dashboard"""
    context = {
        'total_projects': Project.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@login_required
def projects_list(request):
    """List all projects"""
    projects = Project.objects.order_by('-created_at')
    return render(request, 'admin_dashboard/projects_list.html', {'projects': projects})

@login_required
def project_create(request):
    """Create new project"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tech_stack = request.POST.get('tech_stack')
        github_url = request.POST.get('github_url')
        live_url = request.POST.get('live_url')
        is_featured = request.POST.get('is_featured') == 'on'
        image = request.FILES.get('image')
        
        project = Project.objects.create(
            title=title,
            description=description,
            tech_stack=tech_stack,
            github_url=github_url,
            live_url=live_url,
            is_featured=is_featured,
            image=image
        )
        messages.success(request, 'Project created successfully!')
        return redirect('admin_dashboard:projects_list')
    
    return render(request, 'admin_dashboard/project_form.html')

@login_required
def project_edit(request, pk):
    """Edit existing project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.tech_stack = request.POST.get('tech_stack')
        project.github_url = request.POST.get('github_url')
        project.live_url = request.POST.get('live_url')
        project.is_featured = request.POST.get('is_featured') == 'on'
        
        if request.FILES.get('image'):
            project.image = request.FILES.get('image')
        
        project.save()
        messages.success(request, 'Project updated successfully!')
        return redirect('admin_dashboard:projects_list')
    
    return render(request, 'admin_dashboard/project_form.html', {'project': project})

@login_required
def project_delete(request, pk):
    """Delete project"""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('admin_dashboard:projects_list')
    
    return render(request, 'admin_dashboard/project_confirm_delete.html', {'project': project})

@login_required
def about_edit(request):
    """Edit about section"""
    about, created = About.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        about.title = request.POST.get('title')
        about.content = request.POST.get('content')
        about.tech_stack = request.POST.get('tech_stack')
        about.skills = request.POST.get('skills')
        about.cta_text = request.POST.get('cta_text')
        about.cta_url = request.POST.get('cta_url')
        
        if request.FILES.get('profile_image'):
            about.profile_image = request.FILES.get('profile_image')
        
        about.save()
        messages.success(request, 'About section updated successfully!')
        return redirect('admin_dashboard:dashboard')
    
    return render(request, 'admin_dashboard/about_form.html', {'about': about})

@login_required
def home_edit(request):
    """Edit home page content"""
    home, created = HomePage.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        home.hero_title = request.POST.get('hero_title')
        home.hero_subtitle = request.POST.get('hero_subtitle')
        home.hero_cta_text = request.POST.get('hero_cta_text')
        home.hero_cta_url = request.POST.get('hero_cta_url')
        home.tech_stack_title = request.POST.get('tech_stack_title')
        home.tech_stack = request.POST.get('tech_stack')
        home.projects_title = request.POST.get('projects_title')
        home.projects_subtitle = request.POST.get('projects_subtitle')
        
        home.save()
        messages.success(request, 'Home page updated successfully!')
        return redirect('admin_dashboard:dashboard')
    
    return render(request, 'admin_dashboard/home_form.html', {'home': home})

@login_required
def messages_list(request):
    """List all contact messages"""
    messages_list = ContactMessage.objects.order_by('-created_at')
    return render(request, 'admin_dashboard/messages_list.html', {'messages': messages_list})

@login_required
def message_detail(request, pk):
    """View message details"""
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'admin_dashboard/message_detail.html', {'message': message})

@login_required
def message_delete(request, pk):
    """Delete message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('admin_dashboard:messages_list')
    
    return render(request, 'admin_dashboard/message_confirm_delete.html', {'message': message})

@login_required
@csrf_exempt
@require_POST
def ai_rewrite(request):
    """AI text rewriting functionality"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        tone = data.get('tone', 'professional')
        
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        # Call AI API (example with OpenAI-style API)
        api_key = config('AI_API_KEY', default='')
        if not api_key:
            return JsonResponse({'error': 'AI API key not configured'}, status=500)
        
        prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"
        
        # Example API call (adjust based on your AI provider)
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 500,
                'temperature': 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            rewritten_text = result['choices'][0]['message']['content'].strip()
            return JsonResponse({'rewritten_text': rewritten_text})
        else:
            return JsonResponse({'error': 'AI service error'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def login_view(request):
    """Admin login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip_address = request.META.get('REMOTE_ADDR')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f'Successful login for user: {username} from IP: {ip_address}')
            messages.success(request, 'Successfully logged in!')
            return redirect('admin_dashboard:dashboard')
        else:
            logger.warning(f'Failed login attempt for user: {username} from IP: {ip_address}')
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'admin_dashboard/login.html')

def logout_view(request):
    """Admin logout view"""
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('main:home')
