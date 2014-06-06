from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from mock import Mock, patch

from .base import (UserAdminMock, UserAnonymousMock, UserViewerMock,
                   UserContributorMock)
from .base import BaseWebTest
from .base import (PhasesOfPolicyFactory, EnvironmentalThemeFactory,
                   GeographicalScopeFactory)


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class SettingsPolicyPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_phases_of_policy_get_admin(self):
        url = reverse('settings:phases_of_policy')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_phases_of_policy_get_anonymous(self):
        url = reverse('settings:phases_of_policy')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_phases_of_policy_get_viewer(self):
        url = reverse('settings:phases_of_policy')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_phases_of_policy_get_contribuitor(self):
        url = reverse('settings:phases_of_policy')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_phases_of_policy_add_get_admin(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_phases_of_policy_add_get_anonymous(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_phases_of_policy_add_get_viewer(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_phases_of_policy_add_get_contribuitor(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_phases_of_policy_add_post_admin(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_phases_of_policy_add_post_anonymous(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_phases_of_policy_add_post_viewer(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_phases_of_policy_add_post_contribuitor(self):
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_phases_of_policy_edit_get_admin(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_phases_of_policy_edit_get_anonymous(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_phases_of_policy_edit_get_viewer(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_phases_of_policy_edit_get_contribuitor(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_phases_of_policy_edit_post_admin(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_phases_of_policy_edit_post_anonymous(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_phases_of_policy_edit_post_viewer(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_phases_of_policy_edit_post_contribuitor(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class SettingsEnvironmentalThemePermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_environmental_themes_get_admin(self):
        url = reverse('settings:environmental_themes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes.html',
                      resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_environmental_themes_get_anonymous(self):
        url = reverse('settings:environmental_themes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_environmental_themes_get_viewer(self):
        url = reverse('settings:environmental_themes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_environmental_themes_get_contribuitor(self):
        url = reverse('settings:environmental_themes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_environmental_themes_add_get_admin(self):
        url = reverse('settings:environmental_themes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_environmental_themes_add_get_anonymous(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_environmental_themes_add_get_viewer(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_environmental_themes_add_get_contribuitor(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_environmental_themes_add_post_admin(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_environmental_themes_add_post_anonymous(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_environmental_themes_add_post_viewer(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_environmental_themes_add_post_contribuitor(self):
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_environmental_themes_edit_get_admin(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_environmental_themes_edit_get_anonymous(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_environmental_themes_edit_get_viewer(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_environmental_themes_edit_get_contribuitor(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_environmental_themes_edit_post_admin(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_environmental_themes_edit_post_anonymous(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_environmental_themes_edit_post_viewer(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_environmental_themes_edit_post_contribuitor(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)


@override_settings(SKIP_EDIT_AUTH=False, FRAME_URL=True)
class SettingsGeographicalScopesPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_geographical_scopes_get_admin(self):
        url = reverse('settings:geographical_scopes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes.html',
                      resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_geographical_scopes_get_anonymous(self):
        url = reverse('settings:geographical_scopes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_geographical_scopes_get_viewer(self):
        url = reverse('settings:geographical_scopes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_geographical_scopes_get_contribuitor(self):
        url = reverse('settings:geographical_scopes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_geographical_scopes_add_get_admin(self):
        url = reverse('settings:geographical_scopes')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_geographical_scopes_add_get_anonymous(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_geographical_scopes_add_get_viewer(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_geographical_scopes_add_get_contribuitor(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_geographical_scopes_add_post_admin(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_geographical_scopes_add_post_anonymous(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_geographical_scopes_add_post_viewer(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_geographical_scopes_add_post_contribuitor(self):
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_geographical_scopes_edit_get_admin(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_geographical_scopes_edit_get_anonymous(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_geographical_scopes_edit_get_viewer(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_geographical_scopes_edit_get_contribuitor(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAdminMock))
    def test_geographical_scopes_edit_post_admin(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes_edit.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserAnonymousMock))
    def test_geographical_scopes_edit_post_anonymous(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserViewerMock))
    def test_geographical_scopes_edit_post_viewer(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)

    @patch('frame.middleware.requests.get',
           Mock(return_value=UserContributorMock))
    def test_geographical_scopes_edit_post_contribuitor(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('restricted.html', resp.templates[0].name)




