from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('find_jobs', views.find_jobs, name='find_jobs'),
    path('like', views.like, name="like"),
    path('dislike', views.dislike, name="dislike"),


    path('<int:job_id>', views.job_info),
    path('<int:job_id>/note', views.create_note),
    path('<int:job_id>/note_delete/<int:note_id>', views.delete_note),
    path('note_edit/<int:note_id>', views.note_edit, name="note_edit"),
    path('create/<int:user_id>', views.create_job),
    path('post_job/<int:user_id>', views.post_job, name="post_job"),
    path('upload/<int:job_id>', views.upload, name='upload'),
    
    path('profile/<int:user_id>', views.profile),
    
    path('interview_helper/<int:user_id>', views.interview_helper),
    # new path for interview helper using AJAX
    path('interview_helper/<int:user_id>/<str:info_provided>', views.interview_helper_info),
    path('interview_helper/<int:user_id>/<str:info_provided>/update/<int:post_id>', views.interview_helper_info_update),
    path('interview_helper/<int:user_id>/<str:info_provided>/delete/<int:post_id>', views.interview_helper_info_delete),
    
    # profile page Job interests,
    path('job_interest/add/<int:user_id>', views.add_job_interest),
    path('job_interest/<int:pos_id>/delete/<int:user_id>', views.delete_job_interest),
    path('loc_interest/add/<int:user_id>', views.add_loc_interest),
    path('loc_interest/<int:loc_id>/delete/<int:user_id>', views.delete_loc_interest),
    
]