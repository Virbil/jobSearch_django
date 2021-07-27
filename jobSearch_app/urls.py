from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('find_jobs', views.find_jobs, name='find_jobs'),
    # removed paths by Julian
    path('like', views.like, name="like"),
    path('dislike', views.dislike, name="dislike"),
    # new paths made by Archer
    path('<int:job_id>', views.job_info),
    path('<int:job_id>/note', views.create_note),
    path('<int:job_id>/note_delete/<int:note_id>', views.delete_note),
    path('note_edit/<int:note_id>', views.note_edit, name="note_edit"),
    path('create/<int:user_id>', views.create_job),
    path('profile/<int:user_id>', views.profile),
    path('calendar/<int:user_id>', views.calendar),
    path('interview_helper/<int:user_id>', views.interview_helper),
    # new path for interview helper using AJAX
    path('interview_helper/<int:user_id>/<str:info_provided>', views.interview_helper_info),
]