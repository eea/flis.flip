
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from flip.forms import StudyMetadataForm
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

class StudyMetadataEditView(UpdateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'
