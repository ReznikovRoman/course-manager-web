from django.urls import path

from . import views

######################################################################################################################


app_name = 'courses'

urlpatterns = [
    path('teacher/', views.CourseInstanceTeacherListView.as_view(), name='instances-teacher-list'),
    path('teacher/<slug:course_slug>/<slug:instance_slug>/',
         views.CourseInstanceTeacherDetail.as_view(),
         name='course-instance-teacher-detail'),
    path('teacher/<slug:course_slug>/<slug:instance_slug>/enrolls/<int:enroll_pk>/',
         views.EnrollTeacherDetail.as_view(),
         name='enroll-teacher-detail'),
    path('teacher/<slug:course_slug>/<slug:instance_slug>/enrolls/<int:enroll_pk>/assignments/<int:assignment_pk>/',
         views.PersonalAssignmentTeacherDetail.as_view(),
         name='personal-assignment-teacher-detail'),

    path('my-courses/', views.UserCoursesInstancesList.as_view(), name='user-courses'),
    path('', views.CoursesList.as_view(), name='courses-list'),
    path('<slug>/', views.CourseDetail.as_view(), name='course-detail'),

    path('<slug:course_slug>/<slug:instance_slug>/',
         views.CourseInstanceDetail.as_view(),
         name='course-instance-detail'),
    path('<slug:course_slug>/<slug:instance_slug>/unenroll/', views.DeleteEnrollView.as_view(), name='unenroll'),

    path('<slug:course_slug>/<slug:instance_slug>/assignments/<int:pk>/',
         views.PersonalAssignmentDetail.as_view(),
         name='personal-assignment'),



    path('<slug:course_slug>/<slug:instance_slug>/enroll/', views.enroll_view, name='enroll'),
]









