from django.contrib.messages.api import info
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
    jobs = Job.objects.all()
    for j in jobs:
        j.job_desc = ast.literal_eval(j.job_desc)
        j.summary = j.summary.split(";")
        j.summary.pop()
    context = {
        "user_info": logged_user,
        'jobs': jobs,
    }
    return render(request, "home.html", context)

def find_jobs(request):
    positions = Position.objects.all()
    locations = Location.objects.all()
    position = positions[2].__str__()
    location = locations[3].__str__()
    print(position, location)
    
    job_dict = get_jobs(position=position, location=location)
    for job in job_dict.values():
        pos = Position.objects.filter(title=job['JobTitle'])
        if not pos:
            pos = Position.objects.create(title=job["JobTitle"])
        else:
            pos = pos[0]
        Job.objects.create(job_title=pos, company=job['Company'], location=job['Location'], salary_min=job['salary_min'], salary_max=job['salary_max'], job_url=job['JobUrl'], job_desc=job['JobDesc'], summary=job['Summary'])
    return redirect("/job")

@validate_request
def like_job(request, logged_user, like_job_id):
    if request.method == "POST":
        job_to_like = Job.objects.get(id=like_job_id)

        job_to_like.likes.add(logged_user)
    return redirect("/job")

@validate_request
def dislike_job(request, logged_user, dislike_job_id):
    if request.method == "POST":
        job_to_dislike = Job.objects.get(id=dislike_job_id)
        job_to_dislike.dislikes.add(logged_user)
        
        if job_to_dislike.likes.all:
            job_to_dislike.likes.remove(logged_user)
        
    return redirect("/job")

@validate_request
def reset_job(request, logged_user, reset_job_id):
    if request.method == "POST":
        job_to_reset = Job.objects.get(id=reset_job_id)
        
        job_to_reset.likes.remove(logged_user)

        job_to_reset.dislikes.remove(logged_user)
    return redirect("/job")