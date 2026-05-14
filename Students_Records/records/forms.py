from .models import Records
from django.forms import ModelForm

class TaskForm(ModelForm):
    class Meta:
        model = Records
        fields = ['title', 'description', 'date', 'hours_worked']