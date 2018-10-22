from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import activate
from time import gmtime, strftime
from .models import User, Job, Location, Category #make sure to import all other models and migrate
import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def create(request):
    errors = User.objects.validation(request.POST)
    if len(errors):
        for keys, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect('/')
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash)
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard/')
    return redirect('/')


def login(request):
    error = User.objects.login_validation(request.POST)
    if len(error):
        for keys, value in error.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email = request.POST['username']).id
        return redirect('/dashboard/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'jobs': Job.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'first_app/dashboard.html', context)


def job(request, id):
    context={
        'job': Job.objects.get(id=id)
    }
    return render(request,'first_app/view.html', context)


def add_job(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'locations': Location.objects.all()
    }
    return render(request, 'first_app/add_job.html', context)

def process(request):
    errors = Job.objects.job_validation(request.POST)
    if len(errors):
        for keys, value in errors.items():
            messages.error(request, value, extra_tags='new_job')
        return redirect('/jobs/new')
    elif len(request.POST['new_location']) > 3:
        Location.objects.create(location=request.POST['new_location'])
        location = Location.objects.get(location=request.POST['new_location'])
        Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=location, user=User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard/')
    else:
        Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=Location.objects.get(id=request.POST['location']), user=User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard/')


def edit_job(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }
    return render(request, 'first_app/edit_job.html', context)

def edit_process(request, id):
    errors = Job.objects.edit_validation(request.POST)
    if len(errors):
        for keys, value in errors.items():
            messages.error(request, value, extra_tags='new_job')
        return redirect('/jobs/edit/' + id)
    else:
        job = Job.objects.get(id=id)
        job.title = request.POST['title']
        job.desc = request.POST['desc']
        try:
            job.location = Location.objects.get(location=request.POST['location'])
        except:
            Location.objects.create(location=request.POST['location'])
            job.location = Location.objects.get(location=request.POST['location'])
        job.save()
        return redirect('/dashboard/')

def remove(request):
    if 'remove' in request.POST:
        job = Job.objects.get(id=request.POST['job_remove'])
        job.delete()
    return redirect('/dashboard/')

def logout(request):
    request.session.clear()
    return redirect('/')
