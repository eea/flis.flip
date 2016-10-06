from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from mock import Mock, patch

from flip.models import Study
from .base import (UserAdminMock, UserAnonymousMock, UserViewerMock,
                   UserContributorMock)
from .base import BaseWebTest
from .base import StudyFactory, OutcomeFactory


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class StudyMetadataPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_new_get_admin(self):
        url = reverse('study_metadata_add')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/study_add.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_get_anonymous(self):
        url = reverse('study_metadata_add')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_new_post_admin(self):
        url = reverse('study_metadata_add')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/study_add.html', resp.templates[0].name)

    # @patch('frame.middleware.requests.get',
    #        Mock(return_value=UserAdminMock))
    # def test_study_new_saves_logged_user(self):
    #     data = StudyFactory.attributes()
    #     url = reverse('study_metadata_add')
    #     resp = self.app.get(url)
    #     self.assertEqual(200, resp.status_int)
    #     self.assertIn('study/study_add.html', resp.templates[0].name)
    #     form = resp.forms['study-form']
    #     self.populate_fields(form, self.normalize_data(data))
    #     form.submit()
    #     self.assertObjectInDatabase(Study, title=data['title'],
    #                                 user_id='admin')

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_new_get_viewer(self):
        url = reverse('study_metadata_add')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_new_post_viewer(self):
        url = reverse('study_metadata_add')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_view_viewer(self):
        study = StudyFactory()
        url = reverse('study_metadata_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.actions').length)
        self.assertIn('study/metadata_detail', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_view_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(2, resp.pyquery('.actions').length)
        self.assertIn('study/metadata_detail', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_view_different_contribuitor(self):
        study = StudyFactory()
        url = reverse('study_metadata_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.actions').length)
        self.assertIn('study/metadata_detail', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_view_same_contribuitor(self):
        study = StudyFactory(user_id='contribuitor')
        url = reverse('study_metadata_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(2, resp.pyquery('.actions').length)
        self.assertIn('study/metadata_detail', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_view_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_post_anonymous(self):
        url = reverse('study_metadata_add')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_edit_get_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit',
                      kwargs={'study_type': study.study_type, 'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/study_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_get_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit',
                      kwargs={'study_type': study.study_type, 'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_edit_post_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit',
                      kwargs={'study_type': study.study_type, 'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/study_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_post_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit',
                      kwargs={'study_type': study.study_type, 'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_edit_get_by_another_user(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit',
                      kwargs={'study_type': study.study_type, 'pk': study.pk})
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class StudyOutcomePermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcomes_get_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.delete').length)
        self.assertEqual(0, resp.pyquery('#study-outcomes-edit-form').length)
        self.assertIn('study/outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcomes_get_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.delete').length)
        self.assertEqual(0, resp.pyquery('#study-outcomes-edit-form').length)
        self.assertIn('study/outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcomes_get_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcomes_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_get_if_not_blossom(self):
        study = StudyFactory(blossom=Study.NO)
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('outcomes_detail.html', resp.templates[0].name)
        self.assertEqual(0, resp.pyquery('.delete').length)
        self.assertEqual(0, resp.pyquery('#outcome-add').length)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_get_if_blossom(self):
        study = StudyFactory(blossom=Study.YES)
        OutcomeFactory(study=study)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_add_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_add', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcomes_add_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_add', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcomes_add_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_add', kwargs={'pk': study.pk})
        resp = self.app.post(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcomes_add_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        url = reverse('study_outcomes_add', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcomes_add_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_add', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_detail',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(1, resp.pyquery('.actions').length)
        self.assertIn('study/outcome_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcome_get_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_detail',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.actions').length)
        self.assertIn('study/outcome_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_get_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_detail',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('.actions').length)
        self.assertIn('study/outcome_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_get_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_detail',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(1, resp.pyquery('.actions').length)
        self.assertIn('study/outcome_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_detail',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_edit_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcome_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcome_edit_get_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_edit_get_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_edit_get_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcome_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_edit_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_edit_post_admin(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcome_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcome_edit_post_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_edit_post_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.post(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_edit_post_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('study/outcome_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_edit_post_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_edit',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_delete_admin(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_delete',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        redirect_url = reverse('study_metadata_detail',
                               kwargs={'pk': study.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertRedirects(resp, redirect_url)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_study_outcome_delete_viewer(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_delete',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.delete(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_delete_different_contribuitor(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_delete',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.delete(url, expect_errors=True)
        self.assertEqual(404, resp.status_int)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_study_outcome_delete_same_contribuitor(self):
        study = StudyFactory(blossom=Study.YES, user_id='contribuitor')
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_delete',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        redirect_url = reverse('study_metadata_detail',
                               kwargs={'pk': study.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertRedirects(resp, redirect_url)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_delete_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        outcome = OutcomeFactory(study=study)
        url = reverse('study_outcome_delete',
                      kwargs={'pk': study.pk, 'outcome_pk': outcome.pk})
        resp = self.app.delete(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_detail_get_if_blossom(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('outcomes_detail.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_study_outcomes_detail_get_if_not_blossom(self):
        study = StudyFactory(blossom=Study.NO)
        url = reverse('study_outcomes_detail', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertEqual(0, resp.pyquery('#outcome-add').length)
        self.assertIn('outcomes_detail.html', resp.templates[0].name)


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class StudyHomePermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_home_get_admin(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('studies_overview.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_home_get_viewer(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('studies_overview.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_home_get_contribuitor(self):
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
