from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('find_jobs', views.find_jobs, name='find_jobs'),
    path('like_job/<int:like_job_id>', views.like_job, name="like_job"),
    path('dislike_job/<int:dislike_job_id>', views.dislike_job, name="dislike_job"),
    path('reset_job/<int:reset_job_id>', views.reset_job, name="reset_job"),
]