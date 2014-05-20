from datetime import datetime, timedelta

import factory
from factory import fuzzy

from django.core.urlresolvers import reverse
from django_webtest import WebTest
from mock import Mock, patch


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


class StudyFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'flip.Study'

    title = fuzzy.FuzzyText()

    end_date = fuzzy.FuzzyDate(START_DATE, END_DATE)

    lead_author = fuzzy.FuzzyText()

    languages = factory.RelatedFactory('flip.tests.StudyLanguageFactory',
                                       'study')


class LanguageFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'flip.Language'
    FACTORY_DJANGO_GET_OR_CREATE = ('code', 'title')

    code = 'en'
    title = 'English'


class StudyLanguageFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'flip.StudyLanguage'

    language = factory.SubFactory(LanguageFactory)

    study = factory.SubFactory(StudyFactory)

    title = fuzzy.FuzzyText()


class StudyMetadataPermissionTests(WebTest):

    csrf_checks = False

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
    def test_study_edit_get_admin(self):
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
    def test_study_edit_post_admin(self):
        study = StudyFactory()
        url = reverse('study_metadata_edit', kwargs={'pk': study.pk})
        resp = self.app.post(url)
        self.assertEqual(200, resp.status_int)
        self.assertTemplateUsed('restricted.html')
