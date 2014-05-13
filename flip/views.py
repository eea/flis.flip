
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.views.generic import CreateView, UpdateView

from flip.forms import BaseStudyLanguageInlineFormSet
from flip.forms import StudyMetadataForm, StudyContextForm
from flip.models import Study, Outcome, Language, StudyLanguage


class StudyBlossomRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        study = self.get_object()
        if not study.blossom:
            raise Http404
        return super(StudyBlossomRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class StudyLanguageFormMixin(object):

    def get_context_data(self, *args, **kwargs):
        data = super(StudyLanguageFormMixin, self) \
            .get_context_data(*args, **kwargs)
        data['formset'] = self.get_formset(self.request.POST)
        return data

    def get_formset(self, data=None):
        max_num = Language.objects.count()
        extra = 0 if self.object else 1
        StudyLanguageInlineFormSet = inlineformset_factory(
            Study, StudyLanguage,
            formset=BaseStudyLanguageInlineFormSet,
            fields=('language', 'title'),
            extra=extra, max_num=max_num, validate_max=True, can_delete=True)

        if data:
            return StudyLanguageInlineFormSet(data, instance=self.object)
        else:
            return StudyLanguageInlineFormSet(instance=self.object)

    def get_form_kwargs(self):
        kwargs = super(StudyLanguageFormMixin, self).get_form_kwargs()
        kwargs['formset'] = self.get_formset(self.request.POST)
        return kwargs


class StudyMetadataAddView(StudyLanguageFormMixin,
                           CreateView,
                           SuccessMessageMixin):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)


class StudyMetadataEditView(StudyLanguageFormMixin,
                            SuccessMessageMixin,
                            UpdateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return '"{}" study was successfully updated'.format(self.object.title)


class StudyContextEditView(StudyBlossomRequiredMixin,
                           SuccessMessageMixin,
                           UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_context_edit.html'

    def get_success_url(self):
        return reverse('study_context_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        return '"{}" study was successfully updated'.format(self.object.title)


class StudyOutcomesEditView(StudyBlossomRequiredMixin,
                            UpdateView):

    model = Outcome
    form_class = StudyContextForm

    template_name = 'study_outcome_edit.html'
