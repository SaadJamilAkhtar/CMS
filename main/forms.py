from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class SearchFilter(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchFilter, self).__init__(*args, **kwargs)
        groups = Group.objects.all()
        self.group_choice = [(grp.id, grp.name) for grp in groups]
        self.fields['group'] = forms.MultipleChoiceField(choices=self.group_choice, widget=forms.SelectMultiple(
            attrs={'class': 'selectpicker',
                   'data-live-search': 'true'}
        ))


class ExtraFieldForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExtraFieldForm, self).__init__(*args, **kwargs)
        fields = ExtraFields.objects.all()
        for field in fields:
            self.fields[field.field_name] = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control',
                'field_id': field.id
            }), required=False)


class NewFieldForm(forms.ModelForm):
    class Meta:
        model = ExtraFields
        fields = '__all__'
