from datetime import datetime, date, timedelta

from factory import Factory, DjangoModelFactory
from factory import fuzzy
from factory import RelatedFactory, SubFactory

from django.core.urlresolvers import reverse
from django.db.models import Model
from django.db.models.loading import get_model
from django.test.utils import override_settings

from django_webtest import WebTest
from mock import Mock, patch
from webtest.forms import Select, MultipleSelect

from flip.models import Study


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


START_DATE = datetime.now().date()
END_DATE = START_DATE + 5 * timedelta(days=365)


class StudyFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.Study'

    title = fuzzy.FuzzyText()

    blossom = Study.NO

    end_date = fuzzy.FuzzyDate(START_DATE, END_DATE)

    lead_author = fuzzy.FuzzyText()

    languages = RelatedFactory('flip.tests.StudyLanguageFactory', 'study')


class LanguageFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.Language'
    FACTORY_DJANGO_GET_OR_CREATE = ('code', 'title')

    code = 'en'
    title = 'English'


class StudyLanguageFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.StudyLanguage'

    language = SubFactory(LanguageFactory)

    study = SubFactory(StudyFactory)

    title = fuzzy.FuzzyText()


class PhasesOfPolicyFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.PhasesOfPolicy'

    title = fuzzy.FuzzyText()


class EnvironmentalThemeFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.EnvironmentalTheme'

    title = fuzzy.FuzzyText()


class GeographicalScopeFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.GeographicalScope'

    title = fuzzy.FuzzyText()


class StudyContextFactory(Factory):

    ABSTRACT_FACTORY = True

    purpose_and_target = fuzzy.FuzzyChoice([Study.POLICY, Study.NON_POLICY])

    phases_of_policy = SubFactory(PhasesOfPolicyFactory)

    geographical_scope = SubFactory(GeographicalScopeFactory)


class BaseWebTest(WebTest):

    csrf_checks = False

    def populate_fields(self, form, data):
        for field_name, field in form.field_order:
            if field_name in data:
                value = data[field_name]
                if isinstance(value, Model):
                    value = value.pk
                if isinstance(field, MultipleSelect):
                    if not isinstance(value, list):
                        value = [value]
                if isinstance(field, (Select, MultipleSelect)):
                    field.force_value(value)
                else:
                    field.value = value
        return form

    def normalize_data(self, data, date_input_format='%d/%m/%Y'):

        def convert_model_to_pk(value):
            if isinstance(value, Model):
                return value.pk
            return value

        new_data = dict(data)
        for k, v in new_data.items():
            if isinstance(v, list):
                new_data[k] = map(convert_model_to_pk, v)
            elif isinstance(v, date):
                new_data[k] = v.strftime(date_input_format)
            else:
                new_data[k] = convert_model_to_pk(v)
        return new_data

    def assertObjectInDatabase(self, model, **kwargs):
        if isinstance(model, basestring):
            app = kwargs.pop('app', None)
            self.assertTrue(app)
            Model = get_model(app, model)
        else:
            Model = model

        if not Model:
            self.fail('Model {} does not exist'.format(model))
        try:
            return Model.objects.get(**kwargs)
        except Model.DoesNotExist:
            self.fail('Object "{}" with kwargs {} does not exist'.format(
                model, str(kwargs)
            ))


@override_settings(SKIP_EDIT_AUTHORIZATION=True, FRAME_URL=None)
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


@override_settings(SKIP_EDIT_AUTHORIZATION=False, FRAME_URL=True)
class StudyPermissionTests(BaseWebTest):

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_new_get_admin(self):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_get_anonymous(self):
        url = reverse('study_metadata_edit')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_new_post_admin(self):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_new_post_anonymous(self):
        url = reverse('study_metadata_edit')
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_edit_get_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_get_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_edit_post_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_metadata_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_edit_post_anonymous(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_context_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_context_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_context_post_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_context_edit.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_context_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_context_post_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_context_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_study_outcome_get_admin(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('study_outcome.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_study_outcome_get_anonymous(self):
        study = StudyFactory(blossom=Study.YES)
        url = reverse('study_outcomes', kwargs={'pk': study.pk})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAdminMock))
    def test_home_get_admin(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('studies_overview.html')

    @patch('frame.middleware.requests',
           Mock(return_value=UserAnonymousMock))
    def test_home_get_anonymous(self):
        url = reverse('studies_overview')
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')
