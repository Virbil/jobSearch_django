from django.contrib.messages.api import info
from django.db.models.fields import DurationField
from django.http.response import JsonResponse
from jobSearch_app.decorators import validate_request
from django.contrib import messages
from jobSearch_app.models import *
from django.shortcuts import render, redirect
import datetime as dt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .indeed_web_scrape import get_jobs
import ast
import operator
from django.db.models import Q
from functools import reduce
from django.core.files.storage import FileSystemStorage


@validate_request
def home(request, logged_user, jobs=None):
    # filter logic that uses you interests to show you jobs that contain those interest words in the description
    job_interests = ['']
    for value in logged_user.user_pos_saves.all():
        job_interests.append(value.title)
    # print(job_interests)
    filter_job= (Q(job_desc__contains=key_word) for key_word in job_interests)
    job_query = reduce(operator.or_, filter_job)
    # end of interest logic
    
    loc_interests = ['']
    for loc in logged_user.user_loc_saves.all():
        if loc_interests[0] == '':
            loc_interests.pop(0)
            loc_interests.append(f"{loc.city}, {loc.state}")
        else:
            loc_interests.append(f"{loc.city}, {loc.state}")
    # print(loc_interests)
    filter_loc = (Q(location__contains=key_loc) for key_loc in loc_interests)
    loc_query = reduce(operator.or_, filter_loc)
    if not jobs:
        jobs = Job.objects.filter(job_query).filter(loc_query).exclude(dislikes=logged_user).order_by('-post_date')
        # jobs = Job.objects.exclude(dislikes=logged_user).order_by('-post_date')
    else:
        jobs = jobs
    for j in jobs:
        j.job_desc = ast.literal_eval(j.job_desc)
        if j.summary != '':
            if j.summary[-1] == ";":
                j.summary = j.summary.split(";")
                j.summary.pop()        

    context = {
        "user": logged_user,
        'jobs': jobs,
    }
    return render(request, "home.html", context)

@validate_request
def find_jobs(request, logged_user):
    position = request.GET['position']
    location = request.GET['location']
    
    job_dict = get_jobs(position=position, location=location)
    job_ids = []
    for job in job_dict.values():
        pos = Position.objects.filter(title=job['JobTitle'])
        if not pos:
            pos = Position.objects.create(title=job["JobTitle"])
        else:
            pos = pos[0]
        check = Job.objects.filter(job_url=job['JobUrl'])
        if check:
            job_ids.append(check[0].id)
        else:
            job = Job.objects.create(
                job_title=pos, 
                company=job['Company'], 
                location=job['Location'], 
                salary_min=job['salary_min'], 
                salary_max=job['salary_max'], 
                job_url=job['JobUrl'], 
                job_desc=job['JobDesc'], 
                summary=job['Summary'], 
                post_date=job['PostDate']
            )
            job_ids.append(job.id)

    jobs = Job.objects.filter(id__in=job_ids)
    for j in jobs:
        j.summary = j.summary.split(";")
        j.summary.pop()
    context = {
        "user": logged_user,
        'jobs': jobs,
    }
    return render(request, 'home.html', context)

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
        this_user = User.objects.get(id=request.session['userid'])
        this_job = Job.objects.get(id=job_id)
        this_job.job_desc = ast.literal_eval(this_job.job_desc)
        this_job.summary = this_job.summary.split(";")
        this_job.summary.pop()
        context = {
            'this_job': this_job,
            'user': this_user,
        }
        return render(request, 'job-info.html', context)
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

def post_job(request, user_id):
    if 'userid' in request.session:
        user = User.objects.get(id = user_id)
        
        errors = Job.objects.create_job_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/job/create/{user.id}')

        location = request.POST['city'].title() + ',' + request.POST['state'].upper()
        new_position = Position.objects.create(
            title = request.POST['job_title'],
        )
        new_position.pos_saves.add(user)
        new_job = Job.objects.create(
            job_title = new_position,
            company = request.POST['company'],
            location = location,
            post_date = request.POST['post_date'],
            salary_min = request.POST['min'],
            salary_max = request.POST['max'],
            job_url = request.POST['job_url'],
            summary = f"{request.POST['summary']};",
            job_desc = f"{[request.POST['description']]}",
        )

        qualifications = Qualification.objects.create(
            name = request.POST['required'],
            duration = 1
        )
        new_job.qualifications.add(qualifications)
        new_job.likes.add(user)

        return redirect('/job')
    else: 
        return redirect('/')

def profile(request, user_id):
    if 'userid' in request.session:
        logged_user = User.objects.get(id=user_id)
        remote_filter= logged_user.user_loc_saves.filter(city="remote")
        job_likes = logged_user.job_likes.all()      
        for j in job_likes:
            if j.summary:
                if j.summary[-1] == ';':
                    j.summary = j.summary.split(";")
                    j.summary.pop()
                if j.summary[0] == '[':
                    j.summary = ast.literal_eval(j.summary)
        context = {
            "user": logged_user,
            'remote_filter': remote_filter,
            'job_likes': job_likes,
        }
        return render(request, 'profile.html', context)
    else: 
        return redirect('/')

def interview_helper(request, user_id):
    if 'userid' in request.session:
        user = User.objects.get(id=user_id)
        context = {
            "user": User.objects.get(id=user_id),
            'elevator_pitch': ElevatorPitch.objects.filter(creator = user),
            'str_weak': Strength_Weakness.objects.filter(creator = user),
            'accomplishments': Accomplishments.objects.filter(creator = user),
            'common_qa': CommonQA.objects.filter(creator = user),
            'general': General.objects.filter(creator = user)
        }
        return render(request, 'interview-helper.html', context)
    else: 
        return redirect('/')

def interview_helper_info(request, user_id, info_provided):
    if 'userid' in request.session:
        user = User.objects.get(id=user_id)
        if request.method == "POST":
            if info_provided == 'elevator_pitch':
                errors = ElevatorPitch.objects.create_interview_helper_validator(request.POST)
                if len(errors) > 0:
                    for value in errors.values():
                        messages.error(request, value)
                    return redirect(f'/job/interview_helper/{user.id}')

                ElevatorPitch.objects.create(
                    creator = user,
                    elevator_pitch = request.POST['elevator-pitch']
                )
            
            if info_provided == 'str_weak':
                errors = Strength_Weakness.objects.create_interview_helper_validator(request.POST)
                if len(errors) > 0:
                    for value in errors.values():
                        messages.error(request, value)
                    return redirect(f'/job/interview_helper/{user.id}')
                Strength_Weakness.objects.create(
                    creator = user,
                    str_weak = request.POST['str_weak']
                )

            if info_provided == 'accomplishments':
                errors = Accomplishments.objects.create_interview_helper_validator(request.POST)
                if len(errors) > 0:
                    for value in errors.values():
                        messages.error(request, value)
                    return redirect(f'/job/interview_helper/{user.id}')
                Accomplishments.objects.create(
                    creator = user,
                    accomplishments = request.POST['accomplishments']
                )

            if info_provided == 'common_qa':
                errors = CommonQA.objects.create_interview_helper_validator(request.POST)
                if len(errors) > 0:
                    for value in errors.values():
                        messages.error(request, value)
                    return redirect(f'/job/interview_helper/{user.id}')
                CommonQA.objects.create(
                    creator = user,
                    common_qa = request.POST['common_qa']
                )

            if info_provided == 'general':
                errors = General.objects.create_interview_helper_validator(request.POST)
                if len(errors) > 0:
                    for value in errors.values():
                        messages.error(request, value)
                    return redirect(f'/job/interview_helper/{user.id}')
                General.objects.create(
                    creator = user,
                    general = request.POST['general']
                )
            return redirect(f'/job/interview_helper/{user.id}')

    else:
        return redirect('/')

def interview_helper_info_update(request, user_id, info_provided, post_id):
    if 'userid' in request.session:
        user = User.objects.get(id=user_id)

        if request.method == "POST":
            if info_provided == 'elevator_pitch':
                edit_elevator_pitch = ElevatorPitch.objects.get(id = post_id)
                edit_elevator_pitch.elevator_pitch = request.POST['elevator_pitch_edit']
                edit_elevator_pitch.save()
            
            if info_provided == 'str_weak':
                edit_str_weak = Strength_Weakness.objects.get(id = post_id)
                edit_str_weak.str_weak = request.POST['str_weak_edit']
                edit_str_weak.save()

            if info_provided == 'accomplishments':
                edit_accomplishment = Accomplishments.objects.get(id = post_id)
                edit_accomplishment.accomplishments = request.POST['accomplishments_edit']
                edit_accomplishment.save()

            if info_provided == 'common_qa':
                edit_common_qa = CommonQA.objects.get(id = post_id)
                edit_common_qa.common_qa = request.POST['common_qa_edit']
                edit_common_qa.save()

            if info_provided == 'general':
                edit_general = General.objects.get(id = post_id)
                edit_general.general = request.POST['general_edit']
                edit_general.save()

            return redirect(f'/job/interview_helper/{user_id}')

    else:
        return redirect('/')

def interview_helper_info_delete(request, user_id, info_provided, post_id):
    if 'userid' in request.session:
        user = User.objects.get(id=user_id)

        if info_provided == 'elevator_pitch':
            delete_elevator_pitch = ElevatorPitch.objects.get(id = post_id)
            delete_elevator_pitch.delete()
        
        if info_provided == 'str_weak':
            delete_str_week = Strength_Weakness.objects.get(id = post_id)
            delete_str_week.delete()

        if info_provided == 'accomplishments':
            delete_accomplishments = Accomplishments.objects.get(id = post_id)
            delete_accomplishments.delete()

        if info_provided == 'common_qa':
            delete_common_qa = CommonQA.objects.get(id = post_id)
            delete_common_qa.delete()

        if info_provided == 'general':
            delete_general = General.objects.get(id = post_id)
            delete_general.delete()

        return redirect(f'/job/interview_helper/{user_id}')

    else:
        return redirect('/')

def create_note(request, job_id):
    if request.method == 'POST':
        errors = Note.objects.create_note_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/job/{job_id}')
        this_job = Job.objects.get(id=job_id)
        this_user = User.objects.get(id=request.POST['user'])
        Note.objects.create(creator= this_user, job_id=this_job, desc=request.POST['desc'])
        return redirect(f'/job/{job_id}')
    else: 
        return redirect('/')

def note_edit(request, note_id):
    if request.method == "POST":
        this_note = Note.objects.filter(id=note_id)
        errors = Note.objects.create_note_validator(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect(f'/job/{this_note.job_id.id}')
        if this_note:
            this_note = this_note[0]
            this_note.desc = request.POST['desc']
            this_note.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect(f"/job")

def delete_note(request, job_id, note_id):
    if request.method == "POST":
        this_note = Note.objects.get(id=note_id)
        this_note.delete()
        return redirect(f'/job/{job_id}')
    return redirect("/job")


def add_job_interest(request, user_id):
    this_user = User.objects.get(id=user_id)

    errors = Position.objects.create_job_interest_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/job/profile/{user_id}')

    this_job_int = Position.objects.create(
        title = request.POST['title'],
    )
    this_job_int.pos_saves.add(this_user)
    return redirect(f'/job/profile/{user_id}')


def delete_job_interest(request, pos_id, user_id):
    this_pos = Position.objects.get(id=pos_id)
    this_pos.delete()
    return redirect(f'/job/profile/{user_id}')

def add_loc_interest(request, user_id):

    this_user = User.objects.get(id=user_id)

    errors = Location.objects.create_loc_interest_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'/job/profile/{user_id}')

    this_state = State.objects.create(abbr=request.POST['state'])
    this_loc_int = Location.objects.create(
        city = request.POST['city'],
        state = this_state
    )
    # this_loc_int.state.add(request.POST['state'])
    this_loc_int.loc_saves.add(this_user)
    return redirect(f'/job/profile/{user_id}')

def delete_loc_interest(request, loc_id, user_id):
    this_loc = Location.objects.get(id=loc_id)
    this_loc.delete()
    return redirect(f'/job/profile/{user_id}')

# following method MOSTLY from: 
# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
def upload(request, job_id):
    if request.method == 'POST':
        uploaded_file = request.FILES['resume']
        fs = FileSystemStorage()
        file_name = fs.save(uploaded_file.name, uploaded_file)
        request.session['url'] = fs.url(file_name)

    return redirect(f'/job/{job_id}')
