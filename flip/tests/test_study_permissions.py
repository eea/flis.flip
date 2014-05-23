from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from mock import Mock, patch

from flip.models import Study
from .base import (UserAdminMock, UserAnonymousMock, UserViewerMock,
                   UserContributorMock)
from .base import BaseWebTest
from .base import StudyFactory


@override_settings(FRAME_URL=True)
class StudyMetadataPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_new_get_admin(self):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_metadata_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_get_anonymous(self):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_new_post_admin(self):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_metadata_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_new_saves_logged_user(self):
        data = StudyFactory.attributes()
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_metadata_edit.html', resp.templates[0].name)
        form = resp.forms['study-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(Study, title=data['title'],
                                    user_id='admin')

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_new_get_viewer(self):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_new_post_viewer(self):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_post_anonymous(self):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_edit_get_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_metadata_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_get_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_edit_post_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_metadata_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_post_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_edit_get_by_another_user(self):
        study = StudyFactory(user_id='another_user')
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)


@override_settings(FRAME_URL=True)
class StudyContextPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_context_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_context_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_context_post_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_context_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_context_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_context_post_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)


@override_settings(FRAME_URL=True)
class StudyOutcomePermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study_outcome.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_home_get_admin(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('studies_overview.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_home_get_anonymous(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)
