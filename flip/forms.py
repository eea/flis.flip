from django.forms import BooleanField, ModelMultipleChoiceField
from django.forms import DateField, DateInput, ChoiceField, ModelChoiceField
from django.forms import ModelForm, Form
from django.forms.models import BaseInlineFormSet
from django.db.models import Q

from flip.models import (
    Study, Outcome, PhasesOfPolicy, ForesightApproaches, TypeOfOutcome
)
from flis_metadata.common.models import (
    Country, EnvironmentalTheme, GeographicalScope
)


class StudyMetadataForm(ModelForm):

    start_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',),
                           required=False)

    end_date = DateField(widget=DateInput(format='%d/%m/%Y'),
                         input_formats=('%d/%m/%Y',))

    draft = BooleanField(required=False)

    class Meta:
        model = Study
        fields = ('study_type', 'title', 'url', 'blossom',
                  'requested_by', 'start_date', 'end_date', 'draft',
                  'lead_author', 'other', 'purpose_and_target',
                  'additional_information', 'phase_of_policy',
                  'additional_information_phase', 'foresight_approaches',
                  'additional_information_foresight',
                  'stakeholder_participation',
                  'additional_information_stakeholder', 'environmental_themes',
                  'geographical_scope', 'countries')

    def __init__(self, *args, **kwargs):
        self.study = kwargs.get('instance', None)
        self.formset = kwargs.pop('formset', None)
        self.user_id = kwargs.pop('user_id', None)
        super(StudyMetadataForm, self).__init__(*args, **kwargs)
        self.fields['purpose_and_target'].required = True
        self.fields['geographical_scope'].required = True
        self.fields['foresight_approaches'].required = False
        self.fields['study_type'].required = False
        self.fields['geographical_scope'].queryset = (
            GeographicalScope.objects.filter(is_deleted=False))
        self.fields['countries'].queryset = (
            Country.objects.filter(is_deleted=False))
        self.fields['environmental_themes'].queryset = (
            EnvironmentalTheme.objects
            .filter(is_deleted=False)
            .order_by('title')
        )

    def clean(self):
        cleaned_data = super(StudyMetadataForm, self).clean()

        if self.study:
            cleaned_data['study_type'] = self.study.study_type

        if not self.formset.is_valid():
            self._errors['language'] = self.error_class(
                ['Language and original title are required.'])

        start_date_data = cleaned_data.get('start_date')
        blossom_data = cleaned_data.get('blossom')

        start_date = self.fields['start_date']

        if blossom_data == Study.YES:
            if start_date_data in start_date.empty_values:
                self._errors['start_date'] = self.error_class(
                    [start_date.error_messages['required']])
                cleaned_data.pop('start_date', None)

        geographical_scope_data = cleaned_data.get('geographical_scope')
        countries_data = cleaned_data.get('countries')
        countries = self.fields['countries']

        if (geographical_scope_data and
                geographical_scope_data.require_country):
            if len(countries_data) == 0:
                self._errors['countries'] = self.error_class(
                    [countries.error_messages['required']])
                cleaned_data.pop('countries', None)

        if (cleaned_data['study_type'] == 'activity' and
                not cleaned_data['phase_of_policy']):
            self._errors['phase_of_policy'] = self.error_class(
                [self.fields['phase_of_policy'].error_messages['required']])
            cleaned_data.pop('phase_of_policy', None)

        return cleaned_data

    def save(self):
        study = super(StudyMetadataForm, self).save(commit=False)
        study.user_id = self.user_id
        study.save()
        # save languages
        self.formset.save(study)
        self.save_m2m()
        return study


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
        self.fields['type_of_outcome'].queryset = (
            TypeOfOutcome.objects.filter(
                Q(doc_type=self.study.study_type) | Q(doc_type='all')))

    def save(self):
        outcome = super(OutcomeForm, self).save(commit=False)
        outcome.study = self.study
        outcome.save()
        return outcome


class FilterForm(Form):

    BLOSSOM_FILTER_CHOICES = (
        ('', 'All'),
        (Study.YES, 'Blossom'),
        (Study.NO, 'Non-Blossom'),
    )

    blossom = ChoiceField(
        choices=BLOSSOM_FILTER_CHOICES,
        label='Filter entries by')

    phase_of_policy = ModelChoiceField(
        queryset=PhasesOfPolicy.objects.all(),
        empty_label="All policy cycle steps")

    foresight_approaches = ModelMultipleChoiceField(
        queryset=ForesightApproaches.objects.all())

    my_entries = BooleanField()
