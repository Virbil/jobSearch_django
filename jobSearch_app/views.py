from django.contrib.messages.api import info
from django.http.response import JsonResponse
from jobSearch_app.decorators import validate_request
from django.contrib import messages
from jobSearch_app.models import *
from django.shortcuts import render, redirect
import datetime as dt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import json
from .indeed_web_scrape import get_jobs
import ast

@validate_request
def home(request, logged_user):
    jobs = Job.objects.exclude(dislikes=logged_user)
    for j in jobs:
        j.job_desc = ast.literal_eval(j.job_desc)
        j.summary = j.summary.split(";")
        j.summary.pop()
    context = {
        "user": logged_user,
        'jobs': jobs,
    }
    return render(request, "home.html", context)

def find_jobs(request):
    positions = Position.objects.all()
    locations = Location.objects.all()
    position = positions[2].__str__()
    location = locations[0].__str__()
    print(position, location)
    
    job_dict = get_jobs(position=position, location=location)
    for job in job_dict.values():
        pos = Position.objects.filter(title=job['JobTitle'])
        if not pos:
            pos = Position.objects.create(title=job["JobTitle"])
        else:
            pos = pos[0]
        Job.objects.create(job_title=pos, company=job['Company'], location=job['Location'], salary_min=job['salary_min'], salary_max=job['salary_max'], job_url=job['JobUrl'], job_desc=job['JobDesc'], summary=job['Summary'], post_date=job['PostDate'])
    return redirect("/job")

@validate_request
def like_job(request, logged_user, like_job_id):
    if request.method == "POST":
        logged_user = User.objects.get(id=logged_user)
        job_to_like = Job.objects.get(id=like_job_id)
        logged_user.job_likes.add(job_to_like)
        if job_to_like in logged_user.job_dislikes.all():
            logged_user.job_dislikes.remove(logged_user)
    return redirect("/job")

@validate_request
def dislike_job(request, logged_user, dislike_job_id):
    if request.method == "POST":
        logged_user = User.objects.get(id=logged_user)
        job_to_dislike = Job.objects.get(id=dislike_job_id)
        logged_user.dislikes.add(job_to_dislike)
        if job_to_dislike in logged_user.job_likes.all():
            logged_user.job_likes.remove(logged_user)
        
    return redirect("/job")

@validate_request
def reset_job(request, logged_user, reset_job_id):
    if request.method == "POST":
        job_to_reset = Job.objects.get(id=reset_job_id)
        logged_user.job_likes.remove(job_to_reset)
        logged_user.job_dislikes.remove(job_to_reset)
    return redirect("/job")

@validate_request
def like(request, user):
    if request.method == "GET":
        job = Job.objects.filter(id=request.GET['job_id'])
        if job:
            if request.GET['status'] == 'Like':
                user.job_likes.add(job[0])
                user.job_dislikes.remove(job[0])
                data = {'status': "Reset"}
            else:
                user.job_likes.remove(job[0])
                user.job_dislikes.remove(job[0])
                data = {'status': "Like"}
            return JsonResponse(data)
    return redirect("/job")

@validate_request
def dislike(request, user):
    if request.method == "GET":
        job = Job.objects.filter(id=request.GET['job_id'])
        if job:
            if request.GET['status'] == 'Dislike':
                user.job_dislikes.add(job[0])
                user.job_likes.remove(job[0])
                data = {'status': "Reset"}
            else:
                user.job_likes.remove(job[0])
                user.job_dislikes.remove(job[0])
                data = {'status': "Dislike"}
            return JsonResponse(data)
    return redirect("/job")


#Views added by Archer

def job_info(request, job_id):
    if 'userid' in request.session:
        this_job = Job.objects.get(id=job_id)
        this_job.job_desc = ast.literal_eval(this_job.job_desc)
        this_job.summary = this_job.summary.split(";")
        this_job.summary.pop()
        print(this_job.job_desc)
        context = {
            'this_job': this_job,
        }
        return render(request, 'job-info.html', context)
    else: 
        return redirect('/')

def calendar(request, user_id):
    if 'userid' in request.session:
        context = {
            "user": User.objects.get(id=user_id)
        }
        return render(request, 'calendar.html', context)
    else: 
        return redirect('/')

def profile(request, user_id):
    if 'userid' in request.session:

        context = {
            "user": User.objects.get(id=user_id),
        }
        return render(request, 'profile.html', context)
    else: 
        return redirect('/')

def interview_helper(request, user_id):
    if 'userid' in request.session:
        context = {
            "user": User.objects.get(id=user_id),
        }
        return render(request, 'interview-helper.html', context)
    else: 
        return redirect('/')

def create_job(request, user_id):
    if 'userid' in request.session:
        context = {
            "user": User.objects.get(id=user_id),
        }
        return render(request, 'create-job.html', context)
    else: 
        return redirect('/')


