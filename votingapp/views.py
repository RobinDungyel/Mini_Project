from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import PositionForm, RegistrationForm, ChangeForm, CandidateForm,UserForm,VotingTimeForm
from .models import Candidate, ControlVote, Position, Time
from django.utils import timezone
from django.utils.decorators import method_decorator
from .decorators import authorized_user_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
import pytz
from itertools import groupby
from operator import attrgetter
def homeView(request):
    voting_time = Time.objects.first()
    if voting_time:
        now = get_current_time()
        voting_open = voting_time.voting_start <= now <= voting_time.voting_end
        voting_start = voting_time.voting_start.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        voting_end = voting_time.voting_end.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    else:
        voting_open = False
        voting_start = None
        voting_end = None
    return render(request, "home.html", {'voting_open': voting_open, 'voting_start': voting_start, 'voting_end': voting_end})

def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                obj = form.save(commit=False)
                obj.set_password(obj.password)
                obj.save()
                messages.success(request, 'You have been registered. Please login to vote!!')
                return redirect('login')
            else:
                return render(request, "registration.html", {'form': form, 'note': 'password must match'})
    else:
        form = RegistrationForm()
    return render(request, "registration.html", {'form': form})

def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "login.html")
    else:
        return render(request, "login.html")

@login_required
def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
@authorized_user_required
def dashboardView(request):
    voting_time = Time.objects.first()
    voting_open = False
    if voting_time:
        now = get_current_time()
        voting_open = voting_time.voting_start <= now <= voting_time.voting_end
    return render(request, "dashboard.html", {'voting_open': voting_open, 'voting_time': voting_time})

@login_required
@authorized_user_required
def positionView(request):
    positions = Position.objects.all()
    return render(request, "position.html", {'positions': positions})


@login_required
@authorized_user_required
def candidateView(request, pos):
    obj = get_object_or_404(Position, pk=pos)
    candidates = Candidate.objects.filter(position=obj)
    
    if request.method == "POST":
  
            temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]
            if temp.status == False:
                temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
                temp2.total_vote += 1
                temp2.save()
                temp.status = True
                temp.save()
                return HttpResponseRedirect('/position/')
            else:
                messages.success(request, 'you have already been voted this position.')
                return render(request, 'candidate.html', {'obj': obj})
    else:
        return render(request, 'candidate.html', {'obj': obj})

@login_required
@authorized_user_required
def resultView(request):
    voting_time = Time.objects.first()
    now = get_current_time()
    if voting_time and now <= voting_time.voting_end:
        messages.error(request, 'Voting is not yet over.')
        return redirect('dashboard')
    
    positions = Position.objects.all()

    # Prefetch related candidates for each position
    for position in positions:
        position.candidates = position.candidate_set.all()

    # Pass positions to the template
    return render(request, 'result.html', {'positions': positions})
@login_required
@authorized_user_required
def candidateDetailView(request, id):
    obj = get_object_or_404(Candidate, pk=id)
    return render(request, "candidate_detail.html", {'obj': obj})

@login_required
@authorized_user_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "password.html", {'form': form})

@login_required
@authorized_user_required
def editProfileView(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "edit_profile.html", {'form': form})

# Admin
def is_admin(user):
    return user.is_superuser

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_panel')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'admin_login.html')

@user_passes_test(is_admin)
def admin_panel(request):
    positions = Position.objects.all()
    candidates = Candidate.objects.all()
    users = User.objects.all()
    time = Time.objects.all()
    return render(request, 'admin.html', {
        'positions': positions,
        'candidates': candidates,
        'users': users,
        'time': time
    })

@user_passes_test(is_admin)
def add_position(request):
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position added successfully.')
            return redirect('admin_panel')
    else:
        form = PositionForm()
    return render(request, 'add_position.html', {'form': form})

@user_passes_test(is_admin)
def edit_position(request, id):
    position = get_object_or_404(Position, id=id)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, 'Position updated successfully.')
            return redirect('admin_panel')
    else:
        form = PositionForm(instance=position)
    return render(request, 'edit_position.html', {'form': form})

@user_passes_test(is_admin)
def delete_position(request, id):
    position = get_object_or_404(Position, id=id)
    position.delete()
    messages.success(request, 'Position deleted successfully.')
    return redirect('admin_panel')

@user_passes_test(is_admin)
def add_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate added successfully.')
            return redirect('admin_panel')
    else:
        form = CandidateForm()
    return render(request, 'add_candidate.html', {'form': form})

@user_passes_test(is_admin)
def edit_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate updated successfully.')
            return redirect('admin_panel')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'edit_candidate.html', {'form': form})

@user_passes_test(is_admin)
def delete_candidate(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    candidate.delete()
    messages.success(request, 'Candidate deleted successfully.')
    return redirect('admin_panel')

@user_passes_test(is_admin)
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_panel')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

@user_passes_test(is_admin)
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('admin_panel')


# Adjust timezone conversion here
def get_current_time():
    tz = pytz.timezone('Asia/Kolkata')  # Use the same timezone as set in settings.py
    return timezone.now().astimezone(tz)

@user_passes_test(is_admin)
def update_voting_times(request):
    if request.method == "POST":
        form = VotingTimeForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the form data directly to the Time model
            messages.success(request, 'Voting times updated successfully.')
            return redirect('admin_panel')
    else:
        form = VotingTimeForm()
    return render(request, 'update_voting_times.html', {'form': form})
@user_passes_test(is_admin)
def delete_voting_time(request):
    voting_time = Time.objects.first()
    if voting_time:
        voting_time.delete()
        messages.success(request, 'Voting time deleted successfully.')
    else:
        messages.error(request, 'No voting time to delete.')
    return redirect('admin_panel')

@user_passes_test(is_admin)
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('admin_panel')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

