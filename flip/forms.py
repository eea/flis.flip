
from django.forms import DateField, DateInput
from django.forms import ModelForm
from flip.models import Study


class StudyMetadataForm(ModelForm):

    start_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',),
                           required=False)

    end_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                         input_formats=('%d/%m/%Y',))

    class Meta:
        model = Study
        fields = ('title', 'languages', 'title_original', 'url', 'blossom',
                  'requested_by', 'start_date', 'end_date', 'lead_author',
                  'other')

    def __init__(self, *args, **kwargs):
        self.is_draft = kwargs.pop('is_draft', None)
        super(StudyMetadataForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StudyMetadataForm, self).clean()
        requested_by_data = cleaned_data.get('requested_by')
        start_date_data = cleaned_data.get('start_date')
        blossom_data = cleaned_data.get('blossom')

        requested_by = self.fields['requested_by']
        start_date = self.fields['start_date']

        if blossom_data:
            if requested_by_data in requested_by.empty_values:
                self._errors['requested_by'] = self.error_class(
                    [requested_by.error_messages['required']])
                cleaned_data.pop('requested_by', None)
            if start_date_data in start_date.empty_values:
                self._errors['start_date'] = self.error_class(
                    [start_date.error_messages['required']])
                cleaned_data.pop('start_date', None)

        return cleaned_data

    def save(self):
        study = super(StudyMetadataForm, self).save(commit=False)
        study.draft = self.is_draft
        study.save()
        # save relations like languages
        self.save_m2m()
        return study


class StudyContextForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.is_draft = kwargs.pop('is_draft', None)
        super(StudyContextForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Study
        fields = ('purpose_and_target', 'additional_information',
                  'phases_of_policy', 'additional_information_phase',
                  'foresight_approaches', 'stakeholder_participation',
                  'additional_information_stakeholder', 'environmental_themes',
                  'geographical_scope', 'countries')
