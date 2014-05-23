from datetime import datetime, date, timedelta

from django.db.models import Model
from django.db.models.loading import get_model

from django_webtest import WebTest
from factory import Factory, DjangoModelFactory
from factory import fuzzy
from factory import RelatedFactory, SubFactory
from mock import Mock
from webtest.forms import Select, MultipleSelect

from flip.models import Study


USER_ADMIN_DATA = {
    'user_id': 'admin',
    'user_roles': ['Administrator'],
    'groups': []
}
USER_ANONYMOUS_DATA = {
    'user_id': 'anonymous',
    'user_roles': ['Anonymous'],
    'groups': []
}
USER_CONTRIBUTOR_DATA = {
    'user_id': 'contribuitor',
    'user_roles': ['Contributor'],
    'groups': []
}
USER_VIEWER_DATA = {
    'user_id': 'viewer',
    'user_roles': ['Viewer'],
    'groups': []
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


class StudyFactory(DjangoModelFactory):

    FACTORY_FOR = 'flip.Study'

    title = fuzzy.FuzzyText()

    blossom = Study.NO

    end_date = fuzzy.FuzzyDate(START_DATE, END_DATE)

    lead_author = fuzzy.FuzzyText()

    languages = RelatedFactory('flip.tests.base.StudyLanguageFactory', 'study')


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
