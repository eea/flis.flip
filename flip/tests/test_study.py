from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from flip.models import Study
from .base import BaseWebTest
from .base import (StudyFactory)


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class StudyMetadataTests(BaseWebTest):

    # def test_study_metadata_new(self):
    #     StudyFactory()
    #     data = StudyFactory.attributes()
    #     url = reverse('study_metadata_add',
    #                   kwargs={'study_type': 'assessment'})
    #     resp = self.app.get(url)
    #     form = resp.forms['study-form']
    #     self.populate_fields(form, self.normalize_data(data))
    #     form.submit().follow
    #     self.assertObjectInDatabase(Study,
    #                                 title=data['title'],
    #                                 blossom=Study.NO,
    #                                 lead_author=data['lead_author'])

    def test_study_metadata_validate_blossom_and_requested_by(self):
        data = StudyFactory.attributes(extra={'blossom': Study.YES})
        url = reverse('study_metadata_add',
                      kwargs={'study_type': 'assessment'})
        resp = self.app.get(url)
        form = resp.forms['study-form']
        self.populate_fields(form, self.normalize_data(data))
        resp = form.submit()
        self.assertEqual(200, resp.status_int)
        self.assertIn('start_date', resp.context['form'].errors)

    def test_study_metadata_edit(self):
        study = StudyFactory()
        data = StudyFactory.attributes()
        url = reverse('study_metadata_edit', kwargs={'study_type': study.study_type,
                                                     'pk': study.pk})
        resp = self.app.get(url)
        form = resp.forms['study-form']
        data['title'] = 'new title'
        data['geographical_scope'] = study.geographical_scope
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, Study.objects.count())
        self.assertObjectInDatabase(Study,
                                    title=data['title'],
                                    user_id='tester',
                                    lead_author=data['lead_author'])
