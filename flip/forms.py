
from django.forms import ModelForm
from flip.models import Study


class StudyMetadataForm(ModelForm):

    class Meta:
        model = Study
        fields = ('title', 'language', 'title_original', 'url', 'blossom',
                  'requested_by', 'start_date', 'end_date', 'lead_author',
                  'other')
