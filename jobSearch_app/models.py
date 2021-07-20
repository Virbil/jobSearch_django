from django.db import models
from login_reg_app.models import User

class JobManager(models.Manager):

    def position_create_manager(self, post_data):
        errors = {}
        if len(post_data['position']) < 5:
            errors['position'] = "Please make your position more than four characters"
        return errors


class State(models.Model):
    abbr = models.CharField(max_length=45)

    def __str__(self):
        return self.abbr

class Location(models.Model):
    city = models.CharField(max_length=45)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    loc_saves = models.ManyToManyField(User, related_name="user_loc_saves")


    def __str__(self):
        return f"{self.city}, {self.state.abbr}"

class Position(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    pos_saves = models.ManyToManyField(User, related_name="user_pos_saves")

    def __str__(self):
        return f"{self.title}"

class Qualification(models.Model): 
    name = models.CharField(max_length=45)
    duration = models.IntegerField(default=None)
    required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Job(models.Model):
    job_title = models.ForeignKey(Position, on_delete=models.CASCADE)
    company = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    post_date = models.DateField(null=True)
    salary_min = models.IntegerField(blank=True, default=None, null=True)
    salary_max = models.IntegerField(blank=True, default=None)
    job_url = models.CharField(max_length=255)
    job_desc = models.TextField()
    qualifications = models.ManyToManyField(Qualification, related_name="qual_jobs")
    likes = models.ManyToManyField(User, related_name="job_likes")
    dislikes = models.ManyToManyField(User, related_name="job_dislikes")
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title}, {self.company}"

class Note(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, default=None)
    desc = models.TextField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Note by: {self.creator.first_name} {self.creator.last_name} for Job: {self.job_id}"
    





