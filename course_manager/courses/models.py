from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import get_object_or_404

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from accounts import models as account_models


#####################################################################################################################


def student_answers_directory_path(instance, filename):
    return f"assignments/enroll_{instance.enroll.pk}/{filename}"


class Course(models.Model):
    base_title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.base_title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.base_title} Course"


class CourseInstance(models.Model):
    course = models.ForeignKey(Course, related_name='instances', on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True, unique=True)

    sub_title = models.CharField(max_length=100, null=True, blank=True)
    min_mark = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.sub_title:
            self.sub_title = self.course.base_title
        self.slug = slugify(self.sub_title)
        super(CourseInstance, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:course-instance-detail',
                       kwargs={
                           'course_slug': self.course.slug,
                           'instance_slug': self.slug,
                       })

    def __str__(self):
        if self.sub_title == self.course.base_title:
            return f"{self.course} - {self.pk}"
        return f"{self.sub_title}"


class Enroll(models.Model):
    course_instance = models.ForeignKey(CourseInstance, related_name='enrolls', on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.CustomUser', related_name='enrolls', on_delete=models.CASCADE)
    is_course_finished = models.BooleanField(default=False)

    @property
    def average_mark(self):
        marks = [m['grade'] for m in self.personal_assignments.filter(enroll=self).filter(is_completed=True).values('grade')]
        try:
            return round(float(sum(marks) / len(marks)), 2)
        except ZeroDivisionError:
            return 0

    def save(self, *args, **kwargs):
        student_group = Group.objects.get(name='students')
        student_group.user_set.add(self.student)
        super(Enroll, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_instance} - {self.student}"


class Assignment(models.Model):
    title = models.CharField(max_length=100, )
    content = RichTextUploadingField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task: {self.title}"


class CourseInstanceAssignment(Assignment):
    course_instance = models.ForeignKey(CourseInstance, related_name='course_assignments', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            'courses:course-assignment-teacher-detail',
            kwargs={'course_slug': self.course_instance.course.slug,
                    'instance_slug': self.course_instance.slug,
                    'assignment_pk': self.pk}
        )

    def __str__(self):
        return f"Course Task: {self.title}"


class PersonalAssignment(models.Model):
    course_instance_assignment = models.ForeignKey(CourseInstanceAssignment,
                                                   related_name='personal_assignments',
                                                   on_delete=models.CASCADE)
    enroll = models.ForeignKey(Enroll, related_name='personal_assignments', on_delete=models.CASCADE)
    answer_field = models.TextField(null=True, blank=True)
    answer_file = models.FileField(null=True, blank=True, upload_to=student_answers_directory_path)
    is_completed = models.BooleanField(default=False)
    grade = models.SmallIntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    completion_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_deadline_missed(self):
        if self.course_instance_assignment.start_date and self.course_instance_assignment.end_date:
            return self.course_instance_assignment.end_date < timezone.now()
        return False

    @property
    def is_done_after_deadline(self):
        if self.course_instance_assignment.end_date and self.completion_date:
            return self.completion_date > self.course_instance_assignment.end_date
        return False

    def get_absolute_url(self):
        return reverse('courses:personal-assignment',
                       kwargs={
                           'course_slug': self.enroll.course_instance.course.slug,
                           'instance_slug': self.enroll.course_instance.slug,
                           'pk': self.pk
                       })

    def __str__(self):
        return f"Personal Task: {self.course_instance_assignment.title}"


class Certificate(models.Model):
    enroll = models.OneToOneField(Enroll, related_name='certificate', on_delete=models.CASCADE)

    def __str__(self):
        return f"Certificate: {self.enroll.course_instance.sub_title}"

# ==========================  ==========================  ==========================  ==========================  === #
