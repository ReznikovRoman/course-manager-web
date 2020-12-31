from django import forms

from django.core.exceptions import ValidationError

from . import models


####################################################################################################################


class PersonalAssignmentForm(forms.ModelForm):
    class Meta:
        model = models.PersonalAssignment
        fields = ('answer_field', 'answer_file', )

        widgets = {
            'answer_field': forms.Textarea(attrs={'class': 'assignment-text-field'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonalAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['answer_field'].label = 'Enter your answer here'
        self.fields['answer_file'].label = 'Attach file (Optional)'


class PersonalAssignmentEvaluationForm(forms.ModelForm):
    class Meta:
        model = models.PersonalAssignment
        fields = ('grade', 'is_completed')

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        if grade is None or (grade < 0 or grade > 100):
            raise ValidationError('Grade must be in range [0, 100].')
        return grade

    def __init__(self, *args, **kwargs):
        super(PersonalAssignmentEvaluationForm, self).__init__(*args, **kwargs)
        self.fields['grade'].label = 'Grade'
        self.fields['is_completed'].label = 'Mark as completed'












