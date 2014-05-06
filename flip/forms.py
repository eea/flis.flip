
from django.forms import DateField, DateInput
from django.forms import ModelForm
from flip.models import Study


class StudyMetadataForm(ModelForm):

    start_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',))

    end_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                         input_formats=('%d/%m/%Y',))

    class Meta:
        model = Study
        fields = ('title', 'language', 'title_original', 'url', 'blossom',
                  'requested_by', 'start_date', 'end_date', 'lead_author',
                  'other')

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
                del cleaned_data['requested_by']
            if start_date_data in start_date.empty_values:
                self._errors['start_date'] = self.error_class(
                    [start_date.error_messages['required']])
                del cleaned_data['start_date']

        return cleaned_data

    def save(self):
        study = super(StudyMetadataForm, self).save(commit=False)
        study.save()
        return study

