from django.urls import path

from . import views

######################################################################################################################


app_name = 'courses'

urlpatterns = [
    path('my-courses/', views.UserCoursesInstancesList.as_view(), name='user-courses'),
    path('', views.CoursesList.as_view(), name='courses-list'),
    path('<slug>/', views.CourseDetail.as_view(), name='course-detail'),

    path('<slug:course_slug>/<slug:instance_slug>/',
         views.CourseInstanceDetail.as_view(),
         name='course-instance-detail'),
    path('<slug:course_slug>/<slug:instance_slug>/unenroll/', views.DeleteEnrollView.as_view(), name='unenroll'),

    path('<slug:course_slug>/<slug:instance_slug>/<int:pk>/',
         views.PersonalAssignmentDetail.as_view(),
         name='personal-assignment'),

    path('<slug:course_slug>/<slug:instance_slug>/enroll/', views.enroll_view, name='enroll'),
]









