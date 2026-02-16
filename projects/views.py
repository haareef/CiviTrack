from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Project, Branch, SubBranch, ReleasedHistory
from .forms import (UserRegisterForm, UserLoginForm, ProjectForm, 
                    BranchForm, SubBranchForm, ReleasedHistoryForm)


# ═══════════════════════════════════════════════════════════
# PAGE 1 — LOGIN
# ═══════════════════════════════════════════════════════════
def login_view(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user_auth = authenticate(request, username=user.username, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    return redirect('welcome')
                else:
                    messages.error(request, 'Invalid email or password!')
            except User.DoesNotExist:
                messages.error(request, 'User not found!')
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})


# ═══════════════════════════════════════════════════════════
# PAGE 2 — REGISTER
# ═══════════════════════════════════════════════════════════
def register_view(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


# ═══════════════════════════════════════════════════════════
# PAGE 3 — WELCOME
# ═══════════════════════════════════════════════════════════
@login_required
def welcome_view(request):
    return render(request, 'welcome.html')


# ═══════════════════════════════════════════════════════════
# PAGE 4 — PROJECT LIST
# ═══════════════════════════════════════════════════════════
@login_required
def project_list(request):
    projects = request.user.projects.all()
    return render(request, 'project_list.html', {'projects': projects})


# ═══════════════════════════════════════════════════════════
# PAGE 5 — NEW PROJECT
# ═══════════════════════════════════════════════════════════
@login_required
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'new_project.html', {'form': form})


# ═══════════════════════════════════════════════════════════
# PAGE 6 — PROJECT DETAILS
# ═══════════════════════════════════════════════════════════
@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'update_amount':
                try:
                    new_amount = float(request.POST.get('amount', 0))
                    project.amount = new_amount
                    project.save()
                    messages.success(request, 'Project amount updated!')
                except:
                    messages.error(request, 'Invalid amount!')
            
            elif request.POST['action'] == 'release_amount':
                form = ReleasedHistoryForm(request.POST)
                if form.is_valid():
                    release = form.save(commit=False)
                    release.project = project
                    release.save()
                    messages.success(request, 'Amount released successfully!')
                else:
                    messages.error(request, 'Please fill all fields!')
        
        return redirect('project_details', project_id=project_id)
    
    form = ReleasedHistoryForm()
    branches = project.branches.all()
    total_branch_spent = sum(b.total_spent for b in branches)
    remaining = project.amount - project.total_released
    bottom_amount = project.total_released - total_branch_spent
    
    context = {
        'project': project,
        'form': form,
        'branches': branches,
        'total_branch_spent': total_branch_spent,
        'remaining': remaining,
        'bottom_amount': bottom_amount,
    }
    return render(request, 'project_details.html', context)


# ═══════════════════════════════════════════════════════════
# DELETE PROJECT
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    project.delete()
    messages.success(request, 'Project deleted successfully!')
    return redirect('project_list')


# ═══════════════════════════════════════════════════════════
# PAGE 7 — NEW BRANCH
# ═══════════════════════════════════════════════════════════
@login_required
def new_branch(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.project = project
            branch.save()
            messages.success(request, 'Branch created successfully!')
            return redirect('project_details', project_id=project_id)
    else:
        form = BranchForm()
    
    return render(request, 'new_branch.html', {'form': form, 'project': project})


# ═══════════════════════════════════════════════════════════
# DELETE BRANCH
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id, project__user=request.user)
    project = branch.project
    project_id = project.id
    
    # Delete the branch (this will trigger SubBranch deletion via CASCADE)
    branch.delete()
    
    # Recalculate project totals
    project.total_released = sum(rh.amount for rh in project.released_history.all())
    project.save()
    
    messages.success(request, 'Branch and all entries deleted successfully!')
    return redirect('project_details', project_id=project_id)


# ═══════════════════════════════════════════════════════════
# PAGE 8 — BRANCH HISTORY (Sub-Branches)
# ═══════════════════════════════════════════════════════════
@login_required
def branch_history(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id, project__user=request.user)
    project = branch.project
    
    if request.method == 'POST':
        if 'action' in request.POST:
            if request.POST['action'] == 'add':
                form = SubBranchForm(request.POST)
                if form.is_valid():
                    subbranch = form.save(commit=False)
                    subbranch.branch = branch
                    subbranch.save()
                    messages.success(request, 'Sub-branch added successfully!')
                else:
                    messages.error(request, 'Please fill all fields!')
            
            elif request.POST['action'] == 'update_name':
                try:
                    new_name = request.POST.get('name', '')
                    if new_name:
                        branch.name = new_name
                        branch.save()
                        messages.success(request, 'Branch name updated!')
                    else:
                        messages.error(request, 'Branch name cannot be empty!')
                except:
                    messages.error(request, 'Error updating branch name!')
        
        return redirect('branch_history', branch_id=branch_id)
    
    form = SubBranchForm()
    subbranches = branch.subbranches.all()
    
    context = {
        'branch': branch,
        'project': project,
        'form': form,
        'subbranches': subbranches,
    }
    return render(request, 'branch_history.html', context)


# ═══════════════════════════════════════════════════════════
# EDIT SUB-BRANCH
# ═══════════════════════════════════════════════════════════
@login_required
def edit_subbranch(request, subbranch_id):
    subbranch = get_object_or_404(SubBranch, id=subbranch_id, branch__project__user=request.user)
    branch = subbranch.branch
    
    if request.method == 'POST':
        form = SubBranchForm(request.POST, instance=subbranch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sub-branch updated successfully!')
            return redirect('branch_history', branch_id=branch.id)
    else:
        form = SubBranchForm(instance=subbranch)
    
    return render(request, 'edit_subbranch.html', {'form': form, 'subbranch': subbranch, 'branch': branch})


# ═══════════════════════════════════════════════════════════
# DELETE SUB-BRANCH
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def delete_subbranch(request, subbranch_id):
    subbranch = get_object_or_404(SubBranch, id=subbranch_id, branch__project__user=request.user)
    branch = subbranch.branch
    branch_id = branch.id
    
    # Delete the subbranch
    subbranch.delete()
    
    # Recalculate branch total
    branch.recalculate_total_spent()
    
    messages.success(request, 'Entry deleted successfully and amount added back!')
    return redirect('branch_history', branch_id=branch_id)


# ═══════════════════════════════════════════════════════════
# EDIT RELEASED HISTORY
# ═══════════════════════════════════════════════════════════
@login_required
def edit_released_history(request, history_id):
    history = get_object_or_404(ReleasedHistory, id=history_id, project__user=request.user)
    project = history.project
    
    if request.method == 'POST':
        form = ReleasedHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Released history updated successfully!')
            return redirect('released_history', project_id=project.id)
    else:
        form = ReleasedHistoryForm(instance=history)
    
    return render(request, 'edit_released_history.html', {'form': form, 'history': history, 'project': project})


# ═══════════════════════════════════════════════════════════
# DELETE RELEASED HISTORY
# ═══════════════════════════════════════════════════════════
@login_required
@require_POST
def delete_released_history(request, history_id):
    history = get_object_or_404(ReleasedHistory, id=history_id, project__user=request.user)
    project = history.project
    project_id = project.id
    
    # Delete the released history
    history.delete()
    
    # Recalculate project total_released
    project.total_released = sum(rh.amount for rh in project.released_history.all())
    project.save()
    
    messages.success(request, 'Released entry deleted successfully and amount added back!')
    return redirect('released_history', project_id=project_id)


# ═══════════════════════════════════════════════════════════
# PAGE 9 — RELEASED HISTORY
# ═══════════════════════════════════════════════════════════
@login_required
def released_history(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    history = project.released_history.all()
    
    context = {
        'project': project,
        'history': history,
    }
    return render(request, 'released_history.html', context)


# ═══════════════════════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════════════════════
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')
