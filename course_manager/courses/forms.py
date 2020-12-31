from django import forms

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















