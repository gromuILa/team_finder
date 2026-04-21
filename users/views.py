from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings

from .models import User, Skill
from .forms import RegisterForm, LoginForm, EditProfileForm, CustomPasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = User.objects.create_user(
                email=d['email'],
                name=d['name'],
                surname=d['surname'],
                password=d['password'],
            )
            login(request, user)
            return redirect('/projects/list/')
        return render(request, 'users/register.html', {'form': form})
    form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/projects/list/')
        return render(request, 'users/login.html', {'form': form})
    form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/projects/list/')


def user_detail(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user-details.html', {'user': profile_user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES,
            instance=request.user,
            current_user=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect(f'/users/{request.user.pk}/')
        return render(request, 'users/edit_profile.html', {'form': form})
    form = EditProfileForm(instance=request.user, current_user=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(f'/users/{request.user.pk}/')
        return render(request, 'users/change_password.html', {'form': form})
    form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


def participants(request):
    all_skills = Skill.objects.all()
    active_skill = request.GET.get('skill', '')
    qs = User.objects.all().order_by('id')
    if active_skill:
        qs = qs.filter(skills__name=active_skill)
    paginator = Paginator(qs, getattr(settings, 'PAGINATE_BY', 12))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/participants.html', {
        'participants': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill,
        'page_obj': page_obj,
    })


def skills_autocomplete(request):
    q = request.GET.get('q', '')
    skills = Skill.objects.filter(name__istartswith=q).values('id', 'name')[:10]
    return JsonResponse(list(skills), safe=False)


@login_required
def skill_add(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    if request.user != profile_user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    skill_id = request.POST.get('skill_id')
    name = request.POST.get('name', '').strip()
    created = False

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({'error': 'skill_id or name required'}, status=400)

    added = not profile_user.skills.filter(pk=skill.pk).exists()
    if added:
        profile_user.skills.add(skill)

    return JsonResponse({'skill_id': skill.pk, 'created': created, 'added': added})


@login_required
def skill_remove(request, user_id, skill_id):
    profile_user = get_object_or_404(User, pk=user_id)
    if request.user != profile_user:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    skill = get_object_or_404(Skill, pk=skill_id)
    if not profile_user.skills.filter(pk=skill.pk).exists():
        return JsonResponse({'error': 'Skill not in profile'}, status=400)

    profile_user.skills.remove(skill)
    return JsonResponse({'status': 'ok'})
