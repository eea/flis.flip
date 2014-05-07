
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from flip.forms import StudyMetadataForm, StudyContextForm
from flip.models import Study


class StudyMetadataAddView(CreateView, SuccessMessageMixin):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_success_message(self):
        return '{} study was successfully added'.format(self.object.title)

    def get_form_kwargs(self):
        kwargs = super(StudyMetadataAddView, self).get_form_kwargs()
        save = self.request.POST.get('save', 'final')
        kwargs['is_draft'] = True if save == 'draft' else False
        return kwargs


class StudyMetadataEditView(UpdateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'


class StudyContextEditView(UpdateView):

    model = Study
    form_class = StudyContextForm

    template_name = 'study_context_edit.html'
