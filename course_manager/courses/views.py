from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from braces.views import MultiplePermissionsRequiredMixin, GroupRequiredMixin

from . import models as course_models
from accounts import models as account_models
from . import forms


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


class PersonalAssignmentDisplay(LoginRequiredMixin, generic.DetailView):
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
        self.current_assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('pk')
        )

        return self.current_assignment

    def get_context_data(self, **kwargs):
        context = super(PersonalAssignmentDisplay, self).get_context_data(**kwargs)
        context['form'] = forms.PersonalAssignmentForm(
            initial={
                'answer_field': self.current_assignment.answer_field,
                'answer_file': self.current_assignment.answer_file,
            }
        )
        return context


class PersonalAssignmentAnswer(LoginRequiredMixin, SingleObjectMixin, generic.FormView):
    template_name = 'courses/personal_assignment_detail.html'
    form_class = forms.PersonalAssignmentForm
    model = course_models.PersonalAssignment

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(PersonalAssignmentAnswer, self).post(request, *args, **kwargs)

    def form_valid(self, form):
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
        personal_assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('pk')
        )

        assignment_form = forms.PersonalAssignmentForm(self.request.POST)
        personal_assignment.answer_field = assignment_form.data['answer_field']

        try:
            answer_file = self.request.FILES['answer_file']
        except KeyError:
            answer_file = None

        if not personal_assignment.answer_file or answer_file:
            personal_assignment.answer_file = answer_file
        if self.request.POST.getlist('answer_file-clear'):
            personal_assignment.answer_file = None

        personal_assignment.save()
        return super(PersonalAssignmentAnswer, self).form_valid(form)

    def get_success_url(self):
        return reverse('courses:personal-assignment', kwargs={'course_slug': self.kwargs.get('course_slug'),
                                                              'instance_slug': self.kwargs.get('instance_slug'),
                                                              'pk': self.kwargs.get('pk')})


class PersonalAssignmentDetail(LoginRequiredMixin, generic.View):

    def get(self, request, *args, **kwargs):
        view = PersonalAssignmentDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PersonalAssignmentAnswer.as_view()
        return view(request, *args, **kwargs)


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


class PersonalAssignmentTeacherDisplay(LoginRequiredMixin,
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
        self.assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('assignment_pk')
        )
        return self.assignment

    def get_context_data(self, **kwargs):
        context = super(PersonalAssignmentTeacherDisplay, self).get_context_data(**kwargs)
        context['form'] = forms.PersonalAssignmentEvaluationForm(
            initial={
                'grade': self.assignment.grade,
                'is_completed': self.assignment.is_completed,
            }
        )
        return context


class PersonalAssignmentTeacherEvaluate(LoginRequiredMixin,
                                        GroupRequiredMixin,
                                        SingleObjectMixin,
                                        generic.FormView):

    template_name = 'courses/personal_assignment_teacher_detail.html'
    form_class = forms.PersonalAssignmentEvaluationForm
    model = course_models.PersonalAssignment
    group_required = 'teachers'
    context_object_name = 'personal_assignment'

    def post(self, request, *args, **kwargs):
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
        self.object = assignment
        return super(PersonalAssignmentTeacherEvaluate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
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
        personal_assignment = get_object_or_404(
            course_models.PersonalAssignment,
            enroll=enroll,
            pk=self.kwargs.get('assignment_pk')
        )

        mark_form = forms.PersonalAssignmentEvaluationForm(data=self.request.POST)
        if mark_form.is_valid():
            personal_assignment.grade = mark_form.data['grade']
            if self.request.POST.get('is_completed', None):
                personal_assignment.is_completed = True
                if personal_assignment.completion_date is None:
                    personal_assignment.completion_date = timezone.datetime.now()
            else:
                personal_assignment.is_completed = False
                personal_assignment.completion_date = None
            personal_assignment.save()
        return super(PersonalAssignmentTeacherEvaluate, self).form_valid(form)

    def get_success_url(self):
        return reverse('courses:enroll-teacher-detail',
                       kwargs={
                           'course_slug': self.kwargs.get('course_slug'),
                           'instance_slug': self.kwargs.get('instance_slug'),
                           'enroll_pk': self.kwargs.get('enroll_pk'),
                       })


class PersonalAssignmentTeacherDetail(LoginRequiredMixin,
                                      GroupRequiredMixin,
                                      generic.DetailView):
    group_required = 'teachers'

    def get(self, request, *args, **kwargs):
        view = PersonalAssignmentTeacherDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PersonalAssignmentTeacherEvaluate.as_view()
        return view(request, *args, **kwargs)


class CourseAssignmentTeacherDetail(LoginRequiredMixin,
                                    GroupRequiredMixin,
                                    generic.DetailView):

    group_required = 'teachers'
    model = course_models.CourseInstanceAssignment
    template_name = 'courses/course_assignment_teacher_detail.html'
    context_object_name = 'course_assignment'

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        return get_object_or_404(
            course_models.CourseInstanceAssignment,
            course_instance=course_instance,
            pk=self.kwargs.get('assignment_pk')
        )


class CourseAssignmentTeacherCreateView(LoginRequiredMixin,
                                        GroupRequiredMixin,
                                        generic.CreateView):
    group_required = 'teachers'
    model = course_models.CourseInstanceAssignment
    template_name = 'courses/course_instance_assignment_form.html'
    context_object_name = 'course_assignment'
    form_class = forms.CourseAssignmentForm
    
    def form_valid(self, form):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        self.object = form.save(commit=False)
        self.object.course_instance = course_instance
        return super(CourseAssignmentTeacherCreateView, self).form_valid(form)


class CourseAssignmentTeacherUpdateView(LoginRequiredMixin,
                                        GroupRequiredMixin,
                                        generic.UpdateView):
    group_required = 'teachers'
    model = course_models.CourseInstanceAssignment
    template_name = 'courses/course_instance_assignment_form.html'
    context_object_name = 'course_assignment'
    form_class = forms.CourseAssignmentForm

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        return get_object_or_404(
            course_models.CourseInstanceAssignment,
            course_instance=course_instance,
            pk=self.kwargs.get('assignment_pk')
        )

    def get_success_url(self):
        return reverse(
            'courses:course-assignment-teacher-detail',
            kwargs={'course_slug': self.kwargs.get('course_slug'),
                    'instance_slug': self.kwargs.get('instance_slug'),
                    'assignment_pk': self.kwargs.get('assignment_pk')}
        )


class CourseAssignmentTeacherDeleteView(LoginRequiredMixin,
                                        GroupRequiredMixin,
                                        generic.DeleteView):
    group_required = 'teachers'
    model = course_models.CourseInstanceAssignment
    template_name = 'courses/course_assignment_confirm_delete.html'
    context_object_name = 'course_assignment'

    def get_object(self, queryset=None):
        course_instance = get_object_or_404(
            course_models.CourseInstance,
            course__slug=self.kwargs.get('course_slug'),
            slug=self.kwargs.get('instance_slug'),
        )
        return get_object_or_404(
            course_models.CourseInstanceAssignment,
            course_instance=course_instance,
            pk=self.kwargs.get('assignment_pk')
        )

    def get_success_url(self):
        return reverse_lazy(
            'courses:course-instance-teacher-detail',
            kwargs={
                'course_slug': self.kwargs.get('course_slug'),
                'instance_slug': self.kwargs.get('instance_slug'),
            }
        )


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
