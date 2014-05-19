
from django.core.urlresolvers import reverse

from mock import Mock, patch
from django_webtest import WebTest


UserAdminMock = Mock()
UserAdminMock.get.return_value = {
    'user_id': 'admin',
    'user_roles': ['Administrator'],
    'groups': []
}


UserAnonymousMock = Mock()
UserAnonymousMock.get.return_value = {
    'user_id': 'anonymous',
    'user_roles': ['Anonymous'],
    'groups': []
}


class StudyMetadataPermissionTests(WebTest):

    csrf_checks = False

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_new_get_admin(self, mock_requests=None):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_stury_new_get_anonymous(self, mock_requests=None):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_new_post_admin(self, mock_requests=None):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_stury_new_post_anonymous(self, mock_requests=None):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')
