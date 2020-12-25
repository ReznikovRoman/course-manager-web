from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from . import models as course_models
from accounts import models as account_models

##################################################################################################################


class CoursesList(generic.ListView):
    model = course_models.Course
    template_name = 'courses/course_list.html'


class CourseDetail(generic.DetailView):
    model = course_models.Course


class CourseInstanceList(generic.ListView):
    model = course_models.CourseInstance
    template_name = 'courses/course_instance_list.html'

    def get_queryset(self):
        q = course_models.CourseInstance.objects.filter(course__slug=self.kwargs.get('slug'))
        return q


class CourseInstanceDetail(generic.DetailView):
    model = course_models.CourseInstance
    template_name = 'courses/course_instance_detail.html'
    context_object_name = 'course_instance'

    def get_object(self, queryset=None):
        return get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )

    def get_context_data(self, **kwargs):
        context = super(CourseInstanceDetail, self).get_context_data(**kwargs)
        context['is_enrolled'] = self.object.enrolls.filter(student=self.request.user).exists()
        return context


class UserCoursesInstancesList(LoginRequiredMixin, generic.ListView):
    model = course_models.CourseInstance
    template_name = 'courses/user_courses_list.html'
    context_object_name = 'course_instances'

    def get_queryset(self):
        q = course_models.CourseInstance.objects.all().filter(enrolls__student=self.request.user)
        return q

######################################################################################################################


@login_required
def enroll(request, course_slug, instance_slug):
    course_instance = course_models.CourseInstance.objects.get(slug=instance_slug)
    # Create new enroll
    new_enroll = course_models.Enroll.objects.get_or_create(
        course_instance=course_instance,
        student=request.user,
    )
    return HttpResponseRedirect(reverse('courses:courses-list'))




















