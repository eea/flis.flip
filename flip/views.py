
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.views.generic import CreateView, UpdateView

from flip.forms import StudyMetadataForm, StudyContextForm
from flip.models import Language
from flip.models import Study, StudyLanguage


class StudyBlossomRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        study = self.get_object()
        if not study.blossom:
            raise Http404
        return super(StudyBlossomRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class StudyMetadataAddView(CreateView,
                           SuccessMessageMixin):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)

    def get_context_data(self, *args, **kwargs):
        data = super(StudyMetadataAddView, self) \
            .get_context_data(*args, **kwargs)
        data['formset'] = self.get_formset()
        return data

    def get_formset(self, data=None):
        max_num = Language.objects.count()
        StudyLanguageInlineFormSet = inlineformset_factory(
            Study, StudyLanguage,
            fields=('language', 'title'),
            extra=1,
            max_num=max_num,
            validate_max=True,
            can_delete=False)
        if data:
            return StudyLanguageInlineFormSet(data)
        else:
            return StudyLanguageInlineFormSet()

    def get_form_kwargs(self):
        kwargs = super(StudyMetadataAddView, self).get_form_kwargs()
        kwargs['formset'] = self.get_formset(self.request.POST)
        return kwargs


class StudyMetadataEditView(UpdateView,
                            SuccessMessageMixin):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)


class StudyContextEditView(StudyBlossomRequiredMixin,
                           UpdateView,
                           SuccessMessageMixin):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_context_edit.html'

    def get_success_url(self):
        return reverse('study_context_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)


class StudyOutcomesEditView(StudyBlossomRequiredMixin,
                            UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_outcome_edit.html'
