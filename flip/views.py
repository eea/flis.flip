
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


class StudyMetadataEditView(UpdateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})


class StudyContextEditView(StudyBlossomRequiredMixin,
                           UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_context_edit.html'

    def get_success_url(self):
        return reverse('study_context_edit',
                       kwargs={'pk': self.object.pk})


class StudyOutcomesEditView(StudyBlossomRequiredMixin,
                            UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_outcome_edit.html'
