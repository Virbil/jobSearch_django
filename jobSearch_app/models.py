from django.db import models
from login_reg_app.models import User

class JobManager(models.Manager):
    def position_create_manager(self, postData):
        errors = {}
        if len(postData['position']) < 5:
            errors['position'] = "Please make your position more than four characters"
        return errors

class FormManager(models.Manager):
    def create_note_validator(self, postData):
        errors = {}    
        if len(postData['desc']) < 1:
            errors['empty'] = "Note cannot be blank"
        if len(postData['desc']) > 255:
            errors['note'] = "Note cannot be longer than 255 characters"
        return errors


    def create_interview_helper_validator(self, postData):
        errors = {}
        if 'elevator-pitch' in postData:
            if len(postData['elevator-pitch']) < 1:
                errors['elevator_empty'] = "Elevator Pitch cannot be blank"
            if len(postData['elevator-pitch']) > 255:
                errors['elevator_long'] = "Elevator Pitch cannot be longer than 255 characters"
                
        if 'str_weak' in postData:
            if len(postData['str_weak']) < 1:
                errors['str_weak_empty'] = "Strengths and Weaknesses cannot be blank"
            if len(postData['str_weak']) > 255:
                errors['str_weak_long'] = "Strengths and Weaknesses cannot be longer than 255 characters"

        if "accomplishments" in postData:
            if len(postData['accomplishments']) < 1:
                errors['accomplishments_empty'] = "Accomplishments cannot be blank"
            if len(postData['accomplishments']) > 255:
                errors['accomplishments_long'] = "Accomplishments cannot be longer than 255 characters"
        
        if "common_qa" in postData:
            print("it is catching this")
            if len(postData['common_qa']) < 1:
                errors['common_qa_empty'] = "Common Q&A cannot be blank"
            if len(postData['common_qa']) > 255:
                errors['common_qa_long'] = "Common Q&A cannot be longer than 255 characters"

        if "general" in postData:
            print("it is catching this")
            if len(postData['general']) < 1:
                errors['general_empty'] = "General cannot be blank"
            if len(postData['general']) > 255:
                errors['general_long'] = "General cannot be longer than 255 characters"
        return errors

    def create_job_interest_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['interest_empty'] = "cannot be blank"
        if len(postData['title']) > 50:
            errors['interest_long'] = "cannot be longer than 50 characters"
        return errors

    def create_loc_interest_validator(self, postData):
        errors = {}
        if len(postData['city']) < 1:
            errors['city_empty'] = "cannot be blank"
        if len(postData['city']) > 50:
            errors['city_long'] = "cannot be longer than 50 characters"
        if len(postData['state']) < 2:
            errors['state_empty'] = "Must be 2 characters"
        if len(postData['state']) >2:
            errors['state_long'] = "Must be 2 characters"
        return errors

    def create_job_validator(self, postData):
        errors = {}
        if len(postData['company']) < 1:
            errors['company_empty'] = "Company cannot be blank"
        if len(postData['company']) > 50:
            errors['company_long'] = "Company cannot be longer than 50 characters" 

        if len(postData['job_title']) < 1:
            errors['job_title_empty'] = "Job Title cannot be blank"
        if len(postData['job_title']) > 50:
            errors['job_title_long'] = "Job Title cannot be longer than 50 characters" 

        if len(postData['city']) < 1:
            errors['city_empty'] = "City cannot be blank"
        if len(postData['city']) > 50:
            errors['city_long'] = "City cannot be longer than 50 characters"
        if len(postData['state']) < 2:
            errors['state_empty'] = "State must be 2 characters"
        if len(postData['state']) >2:
            errors['state_long'] = "State must be 2 characters"

        if len(postData['post_date']) < 1:
            errors['post_date_empty'] = "Post date cannot be blank"

        if len(postData['job_url']) < 1:
            errors['job_url_empty'] = "URL cannot be blank"

        if len(postData['min']) < 1:
            errors['min_empty'] = "Minimum Salary cannot be blank"
            
        if len(postData['max']) < 1:
            errors['max_empty'] = "Maximum Salary cannot be blank"

        if len(postData['summary']) < 1:
            errors['summary_empty'] = "Summary cannot be blank"
        if len(postData['summary']) > 255:
            errors['summary_long'] = "Summary cannot be longer than 255 characters"

        if len(postData['description']) < 1:
            errors['description_empty'] = "Description cannot be blank"

        return errors


class State(models.Model):
    abbr = models.CharField(max_length=2)
    objects = FormManager()

    def __str__(self):
        return self.abbr

class Location(models.Model):
    city = models.CharField(max_length=45)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    loc_saves = models.ManyToManyField(User, related_name="user_loc_saves")
    objects = FormManager()

    def __str__(self):
        return f"{self.city}, {self.state.abbr}"

class Position(models.Model):
    title = models.CharField(max_length=45, null=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    pos_saves = models.ManyToManyField(User, related_name="user_pos_saves")
    objects = FormManager()
    def __str__(self):
        return f"{self.title}"

class Qualification(models.Model): 
    name = models.CharField(max_length=45)
    duration = models.IntegerField(default=None, null=True)
    required = models.BooleanField(default=False)
    objects = FormManager()

    def __str__(self):
        return f"{self.name}"

class Job(models.Model):
    job_title = models.ForeignKey(Position, on_delete=models.CASCADE)
    company = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    post_date = models.DateField(null=True)
    salary_min = models.IntegerField(blank=True, default=None, null=True)
    salary_max = models.IntegerField(blank=True, default=None, null=True)
    job_url = models.CharField(max_length=255)
    summary = models.CharField(max_length=255, null=True)
    job_desc = models.TextField()
    qualifications = models.ManyToManyField(Qualification, related_name="qual_jobs")
    likes = models.ManyToManyField(User, related_name="job_likes")
    dislikes = models.ManyToManyField(User, related_name="job_dislikes")
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()

    def __str__(self):
        return f"{self.job_title}, {self.company}"

class Note(models.Model):
    creator = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, related_name="notes", on_delete=models.CASCADE, default=None)
    desc = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()

    def __str__(self):
        return f"Note by: {self.creator.first_name} {self.creator.last_name} for Job: {self.job_id}"
    
class ElevatorPitch(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # future/stretch goals to make all fields dynamic (user can add/remove)
    elevator_pitch = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()

class Strength_Weakness(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    str_weak = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()

class Accomplishments(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    accomplishments = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()
    
class CommonQA(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    common_qa = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()
    
class General(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    general = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = FormManager()