from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from flip.models import (PhasesOfPolicy, ForesightApproaches,
                         EnvironmentalTheme, GeographicalScope,
                         TypeOfOutcome)

from .base import BaseWebTest
from .base import (PhasesOfPolicyFactory, ForesightApproachesFactory,
                   EnvironmentalThemeFactory, GeographicalScopeFactory,
                   TypeOfOutcomeFactory)


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class SettingsPolicyTests(BaseWebTest):

    def test_policy_new(self):
        data = PhasesOfPolicyFactory.attributes()
        url = reverse('settings:phases_of_policy_edit')
        resp = self.app.get(url)
        form = resp.forms['policy-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(PhasesOfPolicy, title=data['title'])

    def test_policy_edit(self):
        policy = PhasesOfPolicyFactory()
        data = PhasesOfPolicyFactory.attributes()
        data['title'] = 'new title'
        url = reverse('settings:phases_of_policy_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        form = resp.forms['policy-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, PhasesOfPolicy.objects.count())
        self.assertObjectInDatabase(PhasesOfPolicy, title=data['title'])

    def test_policy_delete_confirm(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_delete',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/policy_confirm_delete.html',
                      resp.templates[0].name)

    def test_policy_delete(self):
        policy = PhasesOfPolicyFactory()
        url = reverse('settings:phases_of_policy_delete',
                      kwargs={'pk': policy.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertEqual(0, PhasesOfPolicy.objects.count())


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class SettingsForesightApproachesTests(BaseWebTest):

    def test_foresight_approaches_new(self):
        data = ForesightApproachesFactory.attributes()
        url = reverse('settings:foresight_approaches_edit')
        resp = self.app.get(url)
        form = resp.forms['foresigh-approaches-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(ForesightApproaches, title=data['title'])

    def test_policy_edit(self):
        policy = ForesightApproachesFactory()
        data = ForesightApproachesFactory.attributes()
        data['title'] = 'new title'
        url = reverse('settings:foresight_approaches_edit',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        form = resp.forms['foresigh-approaches-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, ForesightApproaches.objects.count())
        self.assertObjectInDatabase(ForesightApproaches, title=data['title'])

    def test_policy_delete_confirm(self):
        policy = ForesightApproachesFactory()
        url = reverse('settings:foresight_approaches_delete',
                      kwargs={'pk': policy.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/foresight_approaches_confirm.html',
                      resp.templates[0].name)

    def test_policy_delete(self):
        policy = ForesightApproachesFactory()
        url = reverse('settings:foresight_approaches_delete',
                      kwargs={'pk': policy.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertEqual(0, ForesightApproaches.objects.count())


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class SettingsEnvironmentalThemesTests(BaseWebTest):

    def test_environmental_theme_new(self):
        data = EnvironmentalThemeFactory.attributes()
        url = reverse('settings:environmental_themes_edit')
        resp = self.app.get(url)
        form = resp.forms['environmental-themes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(EnvironmentalTheme, title=data['title'])

    def test_environmental_theme_edit(self):
        theme = EnvironmentalThemeFactory()
        data = EnvironmentalThemeFactory.attributes()
        data['title'] = 'new title'
        url = reverse('settings:environmental_themes_edit',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        form = resp.forms['environmental-themes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, EnvironmentalTheme.objects.count())
        self.assertObjectInDatabase(EnvironmentalTheme, title=data['title'])

    def test_environmental_theme_delete_confirm(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_delete',
                      kwargs={'pk': theme.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/environmental_themes_confirm_delete.html',
                      resp.templates[0].name)

    def test_environmental_theme_delete(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('settings:environmental_themes_delete',
                      kwargs={'pk': theme.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertEqual(0, EnvironmentalTheme.objects.count())


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class SettingsGeographicalScopesTests(BaseWebTest):

    def test_geographical_scopes_new(self):
        data = GeographicalScopeFactory.attributes()
        url = reverse('settings:geographical_scopes_edit')
        resp = self.app.get(url)
        form = resp.forms['geographical-scopes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(GeographicalScope, title=data['title'])

    def test_geographical_scopes_edit(self):
        scope = GeographicalScopeFactory()
        data = GeographicalScopeFactory.attributes()
        data['title'] = 'new title'
        url = reverse('settings:geographical_scopes_edit',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        form = resp.forms['geographical-scopes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, GeographicalScope.objects.count())
        self.assertObjectInDatabase(GeographicalScope, title=data['title'])

    def test_geographical_scopes_delete_confirm(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_delete',
                      kwargs={'pk': scope.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/geographical_scopes_confirm_delete.html',
                      resp.templates[0].name)

    def test_geographical_scopes_delete(self):
        scope = GeographicalScopeFactory()
        url = reverse('settings:geographical_scopes_delete',
                      kwargs={'pk': scope.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertEqual(0, GeographicalScope.objects.count())


@override_settings(SKIP_EDIT_AUTH=True, FRAME_URL=None)
class SettingsOutcomesTests(BaseWebTest):

    def test_geographical_scopes_new(self):
        data = TypeOfOutcomeFactory.attributes()
        url = reverse('settings:outcomes_edit')
        resp = self.app.get(url)
        form = resp.forms['outcomes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertObjectInDatabase(TypeOfOutcome, title=data['title'])

    def test_outcomes_edit(self):
        outcome = TypeOfOutcomeFactory()
        data = TypeOfOutcomeFactory.attributes()
        data['title'] = 'new title'
        url = reverse('settings:outcomes_edit',
                      kwargs={'pk': outcome.pk})
        resp = self.app.get(url)
        form = resp.forms['outcomes-form']
        self.populate_fields(form, self.normalize_data(data))
        form.submit().follow()
        self.assertEqual(1, TypeOfOutcome.objects.count())
        self.assertObjectInDatabase(TypeOfOutcome, title=data['title'])

    def test_outcomes_delete_confirm(self):
        outcome = TypeOfOutcomeFactory()
        url = reverse('settings:outcomes_delete',
                      kwargs={'pk': outcome.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertIn('settings/outcomes_confirm_delete.html',
                      resp.templates[0].name)

    def test_outcomes_delete(self):
        outcome = TypeOfOutcomeFactory()
        url = reverse('settings:outcomes_delete',
                      kwargs={'pk': outcome.pk})
        resp = self.app.delete(url)
        self.assertEqual(302, resp.status_int)
        self.assertEqual(0, TypeOfOutcome.objects.count())

