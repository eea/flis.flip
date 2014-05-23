from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from flip.models import Study
from .base import BaseWebTest
from .base import StudyFactory, EnvironmentalThemeFactory, StudyContextFactory


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class StudyTests(BaseWebTest):

    def test_study_new(self):
        data = StudyFactory.attributes()
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        form = resp.forms['study-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(Study,
                                    title=data['title'],
                                    blossom=Study.NO,
                                    lead_author=data['lead_author'])

    def test_study_validate_blossom_and_requested_by(self):
        data = StudyFactory.attributes(extra={'blossom': Study.YES})
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        form = resp.forms['study-form']
        self.populate_fields(form, self.normalize_data(data))
        resp = form.submit()
        self.assertEqual(200, resp.status_int)
        self.assertIn('start_date', resp.context['form'].errors)
        self.assertIn('requested_by', resp.context['form'].errors)

    def test_study_edit(self):
        study = StudyFactory()
        data = StudyFactory.attributes()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        form = resp.forms['study-form']
        data['title'] = 'new title'
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(Study,
                                    title=data['title'],
                                    blossom=Study.NO,
                                    user_id='tester',
                                    lead_author=data['lead_author'])

    def test_study_context_fail_if_not_blossom_edit(self):
        study = StudyFactory()
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)

    def test_study_context_edit(self):
        study = StudyFactory(blossom=Study.YES)
        env = EnvironmentalThemeFactory()
        data = StudyContextFactory.attributes(
            extra={'environmental_themes': env},
            create=True)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        form = resp.forms['study-context-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(
            Study,
            purpose_and_target=data['purpose_and_target'],
            phases_of_policy=data['phases_of_policy'],
            environmental_themes=data['environmental_themes'],
            geographical_scope=data['geographical_scope'])
