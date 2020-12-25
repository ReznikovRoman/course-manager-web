from django.urls import path

from . import views

######################################################################################################################


app_name = 'courses'

urlpatterns = [
    path('my-courses/', views.UserCoursesInstancesList.as_view(), name='user-courses'),
    path('', views.CoursesList.as_view(), name='courses-list'),
    path('<slug>/', views.CourseDetail.as_view(), name='course-detail'),
    path('<slug>/instances/', views.CourseInstanceList.as_view(), name='available-courses'),

    path('<slug:course_slug>/instances/<slug:instance_slug>/',
         views.CourseInstanceDetail.as_view(),
         name='course-instance-detail'),


    path('<slug:course_slug>/instances/<slug:instance_slug>/enroll/', views.enroll, name='enroll'),
]









