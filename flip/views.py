
from django.views.generic import CreateView
from flip.forms import StudyMetadataForm
from flip.models import Study


class StudyMetadataEditView(CreateView):

    model = Study
    form_class = StudyMetadataForm

    template_name = 'study_metadata_edit.html'
