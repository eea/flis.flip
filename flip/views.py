
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404

from flip.forms import StudyMetadataForm, StudyContextForm
from flip.models import Study


class StudyBlossomRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        study = self.get_object()
        if not study.blossom:
            raise Http404
        return super(StudyBlossomRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class SaveWithDraftOption(object):

    def get_form_kwargs(self):
        kwargs = super(SaveWithDraftOption, self).get_form_kwargs()
        save = self.request.POST.get('save', 'final')
        kwargs['is_draft'] = True if save == 'draft' else False
        return kwargs


class StudyMetadataAddView(SaveWithDraftOption, CreateView,
                           SuccessMessageMixin):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)


class StudyMetadataEditView(SaveWithDraftOption, UpdateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})


class StudyContextEditView(StudyBlossomRequiredMixin, SaveWithDraftOption,
                           UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_context_edit.html'

    def get_success_url(self):
        return reverse('study_context_edit',
                       kwargs={'pk': self.object.pk})


class StudyOutcomesEditView(StudyBlossomRequiredMixin, SaveWithDraftOption,
                            UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_outcome_edit.html'
