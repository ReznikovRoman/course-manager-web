from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from braces.views import MultiplePermissionsRequiredMixin, GroupRequiredMixin

from . import models as course_models
from accounts import models as account_models

##################################################################################################################


class CoursesList(generic.ListView):
    model = course_models.Course
    template_name = 'courses/course_list.html'


class CourseDetail(generic.DetailView):
    model = course_models.Course

    def get_context_data(self, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['available_courses'] = course_models.CourseInstance.objects.filter(course__slug=self.kwargs.get('slug'))
        return context


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
        if not self.request.user.is_authenticated:
            context['is_enrolled'] = False
        else:
            context['is_enrolled'] = self.object.enrolls.filter(student=self.request.user).exists()

        if self.request.user.is_authenticated and context['is_enrolled']:
            context['current_enroll'] = self.object.enrolls.get(student=self.request.user)
        return context


class UserCoursesInstancesList(LoginRequiredMixin, generic.ListView):
    model = course_models.CourseInstance
    template_name = 'courses/user_courses_list.html'
    context_object_name = 'course_instances'

    def get_queryset(self):
        q = course_models.CourseInstance.objects.all().filter(enrolls__student=self.request.user)
        return q


class DeleteEnrollView(LoginRequiredMixin, generic.DeleteView):
    model = course_models.Enroll
    template_name = 'courses/delete_enroll.html'
    success_url = reverse_lazy('courses:user-courses')

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        return get_object_or_404(
            course_models.Enroll,
            course_instance=course_instance,
            student=self.request.user,
        )


class PersonalAssignmentDetail(LoginRequiredMixin, generic.DetailView):
    model = course_models.PersonalAssignment
    template_name = 'courses/personal_assignment_detail.html'
    context_object_name = 'personal_assignment'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        enroll = get_object_or_404(
            course_models.Enroll,
            course_instance=course_instance,
            student=self.request.user,
        )
        assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('pk')
        )

        return assignment


class CourseInstanceTeacherListView(LoginRequiredMixin,
                                    GroupRequiredMixin,
                                    generic.ListView):

    model = course_models.CourseInstance
    group_required = 'teachers'
    template_name = 'courses/course_instance_teacher_list.html'
    context_object_name = 'course_instances'

    def get_queryset(self):
        return get_object_or_404(account_models.Teacher, user=self.request.user).supervised_courses.all()


class CourseInstanceTeacherDetail(LoginRequiredMixin,
                                  GroupRequiredMixin,
                                  generic.DetailView):

    model = course_models.CourseInstance
    group_required = 'teachers'
    template_name = 'courses/course_instance_teacher_detail.html'
    context_object_name = 'course_instance'

    def get_object(self, queryset=None):
        return get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )


class EnrollTeacherDetail(LoginRequiredMixin,
                          GroupRequiredMixin,
                          generic.DetailView):

    model = course_models.Enroll
    group_required = 'teachers'
    template_name = 'courses/enroll_teacher_detail.html'
    context_object_name = 'enroll'

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        return get_object_or_404(
            course_models.Enroll,
            course_instance=course_instance,
            pk=self.kwargs.get('enroll_pk')
        )


class PersonalAssignmentTeacherDetail(LoginRequiredMixin,
                                      GroupRequiredMixin,
                                      generic.DetailView):

    model = course_models.PersonalAssignment
    group_required = 'teachers'
    template_name = 'courses/personal_assignment_teacher_detail.html'
    context_object_name = 'personal_assignment'

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        enroll = get_object_or_404(
            course_models.Enroll,
            course_instance=course_instance,
            pk=self.kwargs.get('enroll_pk'),
        )
        assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('assignment_pk')
        )
        return assignment


######################################################################################################################


@login_required
def enroll_view(request, course_slug, instance_slug):
    course_instance = course_models.CourseInstance.objects.get(slug=instance_slug)

    # Create new enroll
    new_enroll = course_models.Enroll.objects.get_or_create(
        course_instance=course_instance,
        student=request.user,
    )

    return HttpResponseRedirect(reverse('courses:course-instance-detail',
                                        kwargs={
                                            'course_slug': course_instance.course.slug,
                                            'instance_slug': course_instance.slug,
                                        }))
















