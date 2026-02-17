from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
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
# RELEASED HISTORY
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
# EXPORT PROJECT TO PDF
# ═══════════════════════════════════════════════════════════
@login_required
def export_project_pdf(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CiviTrack_{project.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    # Project Header
    story.append(Paragraph(f"CiviTrack - {project.name}", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Summary Section
    story.append(Paragraph("Project Summary", heading_style))
    
    total_spent = sum(b.total_spent for b in project.branches.all())
    remaining = project.amount - project.total_released
    
    summary_data = [
        ['Total Budget', f"Rs. {project.amount:,.2f}"],
        ['Total Released', f"Rs. {project.total_released:,.2f}"],
        ['Total Spent', f"Rs. {total_spent:,.2f}"],
        ['Remaining Balance', f"Rs. {remaining:,.2f}"],
        ['Start Date', str(project.start_date)],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E0E7FF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3 * inch))
    
    # Branches & Expenses Section
    story.append(Paragraph("Branches & Expenses", heading_style))
    
    branches = project.branches.all()
    if branches:
        for branch in branches:
            story.append(Paragraph(f"<b>{branch.name}</b> | Total Spent: Rs. {branch.total_spent:,.2f}", styles['Normal']))
            
            # Sub-branches table
            subbranches_data = [['Expense Name', 'Amount', 'Date']]
            for subbranch in branch.subbranches.all():
                subbranches_data.append([
                    subbranch.name,
                    f"Rs. {subbranch.amount:,.2f}",
                    str(subbranch.date)
                ])
            
            if len(subbranches_data) > 1:
                sb_table = Table(subbranches_data, colWidths=[2.5*inch, 1.2*inch, 1.3*inch])
                sb_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DDD6FE')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
                ]))
                story.append(sb_table)
            else:
                story.append(Paragraph("<i>No expenses recorded</i>", styles['Normal']))
            
            story.append(Spacer(1, 0.15 * inch))
        
        story.append(Spacer(1, 0.2 * inch))
    
    # Released History Section
    story.append(Paragraph("Fund Release History", heading_style))
    
    released = project.released_history.all()
    if released:
        release_data = [['Amount', 'Date']]
        for release in released:
            release_data.append([
                f"Rs. {release.amount:,.2f}",
                str(release.date)
            ])
        
        release_table = Table(release_data, colWidths=[1.5*inch, 1.5*inch])
        release_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D1FAE5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')]),
        ]))
        story.append(release_table)
    else:
        story.append(Paragraph("<i>No fund releases recorded</i>", styles['Normal']))
    
    story.append(Spacer(1, 0.3 * inch))
    
    # Footer
    footer_text = f"<i>Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Exported by: {request.user.email}</i>"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return response


# ═══════════════════════════════════════════════════════════
# LOGOUT
# ═══════════════════════════════════════════════════════════
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')
