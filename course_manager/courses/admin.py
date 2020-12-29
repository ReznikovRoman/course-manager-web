from django.contrib import admin

from django.utils.safestring import mark_safe
from django.urls import reverse

from . import models

#####################################################################################################################


class CourseAdmin(admin.ModelAdmin):
    list_display = ('base_title', 'short_description', 'course_instances_count')
    search_fields = ('base_title', )

    def short_description(self, obj: models.Course):
        return obj.description[:60]

    def course_instances_count(self, obj: models.Course):
        return obj.instances.count()


class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('sub_title', 'base_course_link', 'min_mark', 'start_date', 'end_date', 'enrolls_count')
    search_fields = ('sub_title', 'course__base_title')
    readonly_fields = ('get_teachers', )

    def base_course_link(self, obj: models.CourseInstance):
        return mark_safe(
            f"""<a href="{reverse('admin:courses_course_change', args=(obj.course.pk,))}">{obj.course}</a>"""
        )

    def enrolls_count(self, obj: models.CourseInstance):
        return obj.enrolls.count()

    def get_teachers(self, obj: models.CourseInstance):
        teachers = obj.teachers.all()
        r = ''
        for teacher in teachers:
            r += f"""<a href="{reverse('admin:accounts_teacher_change', args=(teacher.pk,))}">{teacher.profile}</a>; """
        return mark_safe(r)

    get_teachers.short_description = 'teachers'
    base_course_link.short_description = 'base course'


class EnrollAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_instance', 'average_mark', )
    exclude = ('USERNAME_FIELD', )
    search_fields = ('student__email', )
    readonly_fields = ('average_mark', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class MarkAdmin(admin.ModelAdmin):
    list_display = ('value', 'enroll_link',)
    search_fields = ('enroll__course_instance__sub_title', 'enroll__student__email')

    def enroll_link(self, obj: models.Mark):
        return mark_safe(
            f"""<a href="{reverse('admin:courses_enroll_change', args=(obj.assignment.enroll.pk,))}">{obj.assignment.enroll}</a>"""
        )


class CourseInstanceAssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_instance_link', 'start_date', 'end_date')
    list_filter = ('course_instance', )
    search_fields = ('course_instance__sub_title', 'course_instance__course__base_title')

    def course_instance_link(self, obj: models.CourseInstanceAssignment):
        return mark_safe(
            f"""<a href="{reverse('admin:courses_courseinstance_change', args=(obj.course_instance.pk,))}">{obj.course_instance}</a>"""
        )

    course_instance_link.short_description = 'course instance'


class MarkInline(admin.StackedInline):
    model = models.Mark


class PersonalAssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'enroll_link', 'start_date', 'end_date', 'is_completed', 'mark')
    ordering = ('is_completed', )
    search_fields = ('enroll__student__email', )
    readonly_fields = ('enroll_link', )
    list_filter = (
        'enroll__course_instance__course__base_title',
        'enroll__course_instance__sub_title',
    )
    inlines = (MarkInline, )

    def title(self, obj: models.PersonalAssignment):
        return obj.course_instance_assignment.title

    def start_date(self, obj: models.PersonalAssignment):
        return obj.course_instance_assignment.start_date

    def end_date(self, obj: models.PersonalAssignment):
        return obj.course_instance_assignment.end_date

    def enroll_link(self, obj: models.PersonalAssignment):
        return mark_safe(
            f"""{obj.enroll.course_instance} | <a href="{reverse('admin:courses_enroll_change', args=(obj.enroll.pk, ))}">{obj.enroll.student.email}</a>"""
        )

    enroll_link.short_description = 'enroll_link'


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_in', 'enroll_link')
    list_filter = (
        'enroll__course_instance__course__base_title',
        'enroll__course_instance__sub_title',
    )
    search_fields = ('enroll__student__email', )
    readonly_fields = ('enroll_link', )

    def certificate_in(self, obj: models.Certificate):
        return obj.enroll.course_instance.sub_title

    def enroll_link(self, obj: models.Certificate):
        return mark_safe(
            f"""<a href="{reverse('admin:courses_enroll_change', args=(obj.enroll.pk,))}">{obj.enroll}</a>"""
        )

    enroll_link.short_description = 'enroll_link'


######################################################################################################################


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseInstance, CourseInstanceAdmin)
admin.site.register(models.Enroll, EnrollAdmin)
admin.site.register(models.Mark, MarkAdmin)

admin.site.register(models.CourseInstanceAssignment, CourseInstanceAssignmentAdmin)
admin.site.register(models.PersonalAssignment, PersonalAssignmentAdmin)

admin.site.register(models.Certificate, CertificateAdmin)



