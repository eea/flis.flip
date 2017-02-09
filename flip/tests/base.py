from datetime import datetime, date, timedelta

from django.apps import apps
from django.db.models import Model

from django_webtest import WebTest
from factory import Factory, DjangoModelFactory
from factory import fuzzy
from factory import RelatedFactory, SubFactory
from mock import Mock
from webtest.forms import Select, MultipleSelect

from flip import models
from flis_metadata.common import models as common_models

import sys

from django_assets import env as assets_env


USER_ADMIN_DATA = {
    'user_id': 'admin',
    'user_roles': ['Administrator'],
    'groups': [],
    'frame_html': ''
}
USER_ANONYMOUS_DATA = {
    'user_id': 'anonymous',
    'user_roles': ['Anonymous'],
    'groups': [],
    'frame_html': ''
}
USER_CONTRIBUTOR_DATA = {
    'user_id': 'contribuitor',
    'user_roles': ['Contributor'],
    'groups': [],
    'frame_html': ''
}
USER_VIEWER_DATA = {
    'user_id': 'viewer',
    'user_roles': ['Viewer'],
    'groups': [],
    'frame_html': ''
}
UserAdminMock = Mock(status_code=200,
                     json=lambda: USER_ADMIN_DATA)
UserAnonymousMock = Mock(status_code=200,
                         json=lambda: USER_ANONYMOUS_DATA)
UserViewerMock = Mock(status_code=200,
                      json=lambda: USER_VIEWER_DATA)
UserContributorMock = Mock(status_code=200,
                           json=lambda: USER_CONTRIBUTOR_DATA)

START_DATE = datetime.now().date()
END_DATE = START_DATE + 5 * timedelta(days=365)


class LanguageFactory(DjangoModelFactory):

    class Meta:
        model = models.Language
        django_get_or_create = ('code', 'title')

    code = 'en'
    title = 'English'


class PhasesOfPolicyFactory(DjangoModelFactory):

    class Meta:
        model = models.PhasesOfPolicy

    title = fuzzy.FuzzyText()


class ForesightApproachesFactory(DjangoModelFactory):

    class Meta:
        model = models.ForesightApproaches

    title = fuzzy.FuzzyText()


class EnvironmentalThemeFactory(DjangoModelFactory):

    class Meta:
        model = common_models.EnvironmentalTheme

    title = fuzzy.FuzzyText()


class GeographicalScopeFactory(DjangoModelFactory):

    class Meta:
        model = common_models.GeographicalScope

    title = fuzzy.FuzzyText()

    require_country = False


class StudyContextFactory(Factory):
    ABSTRACT_FACTORY = True

    purpose_and_target = fuzzy.FuzzyChoice([models.Study.POLICY,
                                            models.Study.NON_POLICY])

    phase_of_policy = SubFactory(PhasesOfPolicyFactory)

    geographical_scope = SubFactory(GeographicalScopeFactory)

    foresight_approaches = SubFactory(ForesightApproachesFactory)


class TypeOfOutcomeFactory(DjangoModelFactory):

    class Meta:
        model = models.TypeOfOutcome

    title = fuzzy.FuzzyText()
    doc_type = fuzzy.FuzzyChoice([models.Study.ACTIVITY,
                                  models.Study.ASSESSMENT])


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
            Model = apps.get_model(app, model)
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

    def tearDown(self):
        # This is a hack to fix this issue:
        # https://github.com/miracle2k/django-assets/issues/44
        assets_env.reset()
        assets_env._ASSETS_LOADED = False
        if 'flip.modules' in sys.modules:
            del sys.modules['flip.assets']
        super(BaseWebTest, self).tearDown()


class StudyFactory(DjangoModelFactory):

    class Meta:
        model = models.Study

    title = fuzzy.FuzzyText()

    blossom = models.Study.NO

    end_date = fuzzy.FuzzyDate(START_DATE, END_DATE)

    lead_author = fuzzy.FuzzyText()

    languages = RelatedFactory('flip.tests.base.StudyLanguageFactory', 'study')

    study_type = 'assessment'

    purpose_and_target = fuzzy.FuzzyChoice([models.Study.POLICY,
                                            models.Study.NON_POLICY])

    geographical_scope = SubFactory(GeographicalScopeFactory)


class StudyLanguageFactory(DjangoModelFactory):

    class Meta:
        model = models.StudyLanguage

    language = SubFactory(LanguageFactory)

    study = SubFactory(StudyFactory)

    title = fuzzy.FuzzyText()


class OutcomeFactory(DjangoModelFactory):

    class Meta:
        model = models.Outcome

    study = SubFactory(StudyFactory)

    type_of_outcome = SubFactory(TypeOfOutcomeFactory)

    document_title = fuzzy.FuzzyText()
