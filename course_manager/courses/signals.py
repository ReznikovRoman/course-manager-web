from django.dispatch import receiver
from django.db.models.signals import (post_save, )

from . import models


#######################################################################################################################


@receiver(post_save, sender=models.Enroll)
def create_enroll(sender, instance: models.Enroll, created, **kwargs):
    if created:
        for assignment in instance.course_instance.course_assignments.all():
            models.PersonalAssignment.objects.get_or_create(
                course_instance_assignment=assignment,
                enroll=instance,
            )


@receiver(post_save, sender=models.Enroll)
def update_assignments(sender, instance: models.Enroll, created: bool, **kwargs):
    if not created:
        for assignment in instance.course_instance.course_assignments.all():
            assignment.save()


@receiver(post_save, sender=models.CourseInstanceAssignment)
def add_new_course_assignment(sender, instance: models.CourseInstanceAssignment, created: bool, **kwargs):
    if created:
        enrolls = instance.course_instance.enrolls.all()
        if enrolls:
            for enroll in enrolls:
                models.PersonalAssignment.objects.get_or_create(
                    course_instance_assignment=instance,
                    enroll=enroll,
                )


@receiver(post_save, sender=models.CourseInstanceAssignment)
def update_course_assignment(sender, instance: models.CourseInstanceAssignment, created: bool, **kwargs):
    if not created:
        enrolls = instance.course_instance.enrolls.all()
        if enrolls:
            for enroll in enrolls:
                for personal_assignment in enroll.personal_assignments.all():
                    personal_assignment.save()


@receiver(post_save, sender=models.Mark)
def add_new_mark(sender, instance: models.Mark, created: bool, **kwargs):
    if created:
        personal_assignment = instance.assignment
        personal_assignment.is_completed = True
        personal_assignment.save()



