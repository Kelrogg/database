from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from web.models import Meeting, Prisoner, User, Admin
from django import forms


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ["meetingcol", "theme", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "meetingcol": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название события"}
            ),
            "theme": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание события",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    def __init__(self, queryset, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=queryset)

    class Meta:
        model = Prisoner
        fields = ['user']