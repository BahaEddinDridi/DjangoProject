from django import forms
from .models import TrainingPlan, ExerciseSet, Exercise

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'exercises']

class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'sets', 'repetitions', 'rest_time']

    def __init__(self, *args, **kwargs):
        super(ExerciseSetForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        empty_label="Select an Exercise"
    )
    sets = forms.IntegerField(
        min_value=1,
        help_text="Enter the number of sets (minimum 1)."
    )
    repetitions = forms.IntegerField(
        min_value=1,
        help_text="Enter the number of repetitions (minimum 1)."
    )
    rest_time = forms.DurationField(
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM:SS'}),
        help_text="Enter duration in format: HH:MM:SS"
    )

    def clean_rest_time(self):
        rest_time = self.cleaned_data.get('rest_time')
        if not rest_time:
            raise forms.ValidationError("This field cannot be empty.")
        return rest_time
