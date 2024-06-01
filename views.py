# Django (web framework) imports
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import Chain, Block

# Python module imports
import datetime as dt
import hashlib

#Blockchain imports

from .blockchain import generate_next, create_genesis_block, add_block, check_integrity

# This function displays the home/login page of the website and handles the login of the user.
def home(request):
    if request.method=='GET':
        return render(request, "login.html", {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, "login.html", {'form':AuthenticationForm, 'error':"Username and password did not match."})
        else:
            login(request, user)
            return redirect('dashboard')

# This function displays the registration page of the website and handles the registration of a new user.
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'forms':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'register.html', {'forms':UserCreationForm(), 'error':"Username has already been taken, try another one."})
        else:
            return render(request, 'register.html', {'forms':UserCreationForm(), 'error':"Passwords don't match."})


# This function helps the user log out.
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# This function displays the dashboard page of the website.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def dashboard(request):
    chains = Chain.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'chains':chains})

# This function displays the course creation page of the website.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def create_course(request):
    if request.method == 'GET':
        return render(request, 'create_course.html', {})
    elif request.method == 'POST':    
        name=request.POST['name']
        year=request.POST['year']
        sem=request.POST['sem']
        code=request.POST['code']
        slot=request.POST['slot']
        strength=request.POST['strength']
        newchain = Chain(
            name=name,
            year=year,
            sem=sem,
            code=code,
            slot=slot,
            strength=strength
        )
        newchain.user = request.user
        newchain.save()
        block = create_genesis_block(request, chain_id=newchain.pk)
        block.save()
        return redirect('success')

# This function displays the success page after a new course is created successfully.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def success(request):
    return render(request, 'success.html', {'announcements':"Success! The new course chain has been created."})

# This function displays all the courses of the user on the page.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def course_view(request, chain_id):
    chain = Chain.objects.get(pk=chain_id)
    blocks = Block.objects.filter(chain=chain).order_by('-timestamp')
    return render(request, 'course_view.html', {'blocks':blocks,"chain":chain})

# This function displays the roll numbers and accepts the attendance status inputs.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def mark_attendance(request, chain_id):
    if request.method== 'GET':
        chain = Chain.objects.get(pk=chain_id)
        number = []
        for i in range(int(chain.strength)):
            number.append(i+1)
        return render(request, 'mark_attendance.html', {'chain':chain, 'number':number})
    else:
        chain = Chain.objects.get(pk=chain_id)
        block_to_add = add_block(request, chain)
        block_to_add.save()
        return redirect('course_view', chain_id)

# This function displays the attendance of all the students in a particular period.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def attendance_view(request, chain_id, block_id):
    block = Block.objects.get(pk=block_id)
    chain = Chain.objects.get(pk=chain_id)
    sd = []
    for i in range(len(block.data[:])):
        if block.data[i].isalpha():
            sd.append(block.data[i])

    return render(request, 'attendance_view.html', {'block':block, 'chain':chain, 'sd':sd})

# This function displays whether the integrity of the particular chain has been maintained.
# The decorator '@login_required' ensures the page is only available to a logged in user.
@login_required(login_url='/')
def integrity(request, chain_id):
    chain = Chain.objects.get(pk=chain_id)
    length = Block.objects.filter(chain=chain).count()
    hashes = []
    prev_hashes = []
    for i in range(length):
        hashes.append(Block.objects.filter(chain=chain).order_by('index')[i].block_hash)
        prev_hashes.append(Block.objects.filter(chain=chain).order_by('index')[i].prev_hash)
    
    result = check_integrity(hashes, prev_hashes, length)
    if result == "Not modified":
        return render(request, 'integrity.html', {'announcements':"The integrity of the chain has been maintained."})
    else:
        return render(request, 'integrity.html', {'announcements':result})
        
