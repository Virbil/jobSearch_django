from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('find_jobs', views.find_jobs, name='find_jobs'),
    path('like_job/<int:like_job_id>', views.like_job, name="like_job"),
    path('dislike_job/<int:dislike_job_id>', views.dislike_job, name="dislike_job"),
    path('reset_job/<int:reset_job_id>', views.reset_job, name="reset_job"),
    path('like', views.like, name="like"),
    path('dislike', views.dislike, name="dislike"),
    # new paths made by Archer
    path('<int:job_id>', views.job_info),
    path('create/<int:user_id>', views.create_job),
    path('profile/<int:user_id>', views.profile),
    path('calendar/<int:user_id>', views.calendar),
    path('interview_helper/<int:user_id>', views.interview_helper),
]