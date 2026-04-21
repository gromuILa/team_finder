from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings

from .models import Project
from .forms import ProjectForm


def project_list(request):
    qs = Project.objects.select_related('owner').order_by('-created_at')
    paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 12))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'projects/project_list.html', {
        'projects': page_obj,
        'page_obj': page_obj,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect(f'/projects/{project.pk}/')
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})
    form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.owner and not request.user.is_staff:
        return redirect(f'/projects/{project_id}/')
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(f'/projects/{project_id}/')
        return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})
    form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
def project_complete(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.owner and not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if project.status != 'open':
        return JsonResponse({'error': 'Project already closed'}, status=400)
    project.status = 'closed'
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': 'closed'})


@login_required
def toggle_participate(request, project_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participating = False
    else:
        project.participants.add(user)
        participating = True
    return JsonResponse({'status': 'ok', 'participating': participating})
