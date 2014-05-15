
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from flip.forms import BaseStudyLanguageInlineFormSet
from flip.forms import StudyMetadataForm, StudyContextForm, OutcomeForm
from flip.models import Study, Language, StudyLanguage, Outcome


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
        return 'The study was successfully added'


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
        return 'The study was successfully updated'


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
        return 'The study was successfully updated'


class StudyOutcomesEditView(StudyBlossomRequiredMixin,
                            SuccessMessageMixin,
                            CreateView):

    model = Outcome
    form_class = OutcomeForm
    template_name = 'study_outcome_edit.html'

    def dispatch(self, request, pk):
        self._object = self.get_object()
        return super(StudyOutcomesEditView, self).dispatch(request, pk)

    def get_object(self):
        return get_object_or_404(Study, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super(StudyOutcomesEditView, self).get_context_data(**kwargs)
        data['object'] = self._object
        return data

    def get_form_kwargs(self):
        kwargs = super(StudyOutcomesEditView, self).get_form_kwargs()
        kwargs['study'] = self._object
        return kwargs

    def get_success_url(self):
        return reverse('study_outcomes_edit', kwargs={'pk': self._object.pk})

    def get_success_message(self, cleaned_data):
        return '{document_title} was successfully added'.format(**cleaned_data)


class StudyOutcomesDeleteView(DeleteView):

    model = Outcome
    pk_url_kwarg = 'outcome_pk'
    template_name = 'outcome_confirm_delete.html'

    def dispatch(self, request, pk, outcome_pk):
        self.study = get_object_or_404(Study, pk=pk)
        return super(StudyOutcomesDeleteView, self).dispatch(request, pk)

    def get_success_url(self):
        return reverse('study_outcomes_edit', kwargs={'pk': self.study.pk})

    def get_context_data(self, **kwargs):
        data = super(StudyOutcomesDeleteView, self).get_context_data(**kwargs)
        data['study'] = self.study
        return data


class HomeView(ListView):

    model = Study
    template_name = 'studies_overview.html'
