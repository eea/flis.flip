
from django.forms import BooleanField, ModelMultipleChoiceField
from django.forms import DateField, DateInput, ChoiceField, ModelChoiceField
from django.forms import ModelForm, Form
from django.forms.models import BaseInlineFormSet

from flip.models import Study, Outcome, PhasesOfPolicy, ForesightApproaches


class StudyMetadataForm(ModelForm):

    start_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',),
                           required=False)

    end_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                         input_formats=('%d/%m/%Y',))

    draft = BooleanField(required=False)

    class Meta:
        model = Study
        fields = ('title', 'url', 'blossom',
                  'requested_by', 'start_date', 'end_date', 'draft',
                  'lead_author', 'other')

    def __init__(self, *args, **kwargs):
        self.formset = kwargs.pop('formset', None)
        self.user_id = kwargs.pop('user_id', None)
        super(StudyMetadataForm, self).__init__(*args, **kwargs)
        self.fields['blossom'].initial = ''

    def clean(self):
        cleaned_data = super(StudyMetadataForm, self).clean()

        if not self.formset.is_valid():
            self._errors['language'] = self.error_class(
                ['Language and original title are required.'])

        requested_by_data = cleaned_data.get('requested_by')
        start_date_data = cleaned_data.get('start_date')
        blossom_data = cleaned_data.get('blossom')

        requested_by = self.fields['requested_by']
        start_date = self.fields['start_date']

        if blossom_data == Study.YES:
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
        study.user_id = self.user_id
        study.save()
        # save languages
        self.formset.save(study)
        return study


class StudyContextForm(ModelForm):

    draft = BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(StudyContextForm, self).__init__(*args, **kwargs)

        self.fields['purpose_and_target'].required = True
        self.fields['phase_of_policy'].required = True
        self.fields['environmental_themes'].required = True
        self.fields['geographical_scope'].required = True

    def clean(self):
        cleaned_data = super(StudyContextForm, self).clean()
        geographical_scope_data = cleaned_data.get('geographical_scope')
        countries_data = cleaned_data.get('countries')
        countries = self.fields['countries']

        if (geographical_scope_data and
            geographical_scope_data.require_country):
            if len(countries_data) == 0:
                self._errors['countries'] = self.error_class(
                    [countries.error_messages['required']])
                cleaned_data.pop('countries', None)

        return cleaned_data

    class Meta:
        model = Study
        fields = ('draft', 'purpose_and_target', 'additional_information',
                  'phase_of_policy', 'additional_information_phase',
                  'foresight_approaches', 'additional_information_foresight',
                  'stakeholder_participation',
                  'additional_information_stakeholder', 'environmental_themes',
                  'geographical_scope', 'countries')


class BaseStudyLanguageInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseStudyLanguageInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def save(self, study):
        study_languages = super(BaseStudyLanguageInlineFormSet, self) \
            .save(commit=False)
        for study_language in study_languages:
            study_language.study = study
            study_language.save()
        return study_languages


class OutcomeForm(ModelForm):

    class Meta:
        model = Outcome
        exclude = ('study',)

    def __init__(self, *args, **kwargs):
        self.study = kwargs.pop('study', None)
        super(OutcomeForm, self).__init__(*args, **kwargs)

    def save(self):
        outcome = super(OutcomeForm, self).save(commit=False)
        outcome.study = self.study
        outcome.save()
        return outcome


class FilterForm(Form):

    BLOSSOM_FILTER_CHOICES = (
        ('', 'All studies'),
        (Study.YES, 'Blossom'),
        (Study.NO, 'Non-Blossom'),
    )

    blossom = ChoiceField(
        choices=BLOSSOM_FILTER_CHOICES,
        label='Filter studies by')

    phase_of_policy = ModelChoiceField(
        queryset=PhasesOfPolicy.objects.all(),
        empty_label="All policy cycle steps")

    foresight_approaches = ModelMultipleChoiceField(
        queryset=ForesightApproaches.objects.all())

    my_entries = BooleanField()
