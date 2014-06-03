from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from flip import views


admin.autodiscover()


settings_urls = patterns(

    '',

    url(r'^phases_of_policy/$',
        views.SettingsPhasesOfPolicyView.as_view(),
        name='phases_of_policy'),

    url(r'^phases_of_policy/new/$',
        views.SettingsPhasesOfPolicyAddView.as_view(),
        name='phases_of_policy_edit'),

    url(r'^phases_of_policy/(?P<pk>\d+)/edit$',
        views.SettingsPhasesOfPolicyEditView.as_view(),
        name='phases_of_policy_edit'),

)


study_urls = patterns(

    '',

    url(r'^new/$',
        views.StudyMetadataAddView.as_view(),
        name='study_metadata_edit'),

    url(r'^(?P<pk>\d+)/edit$',
        views.StudyMetadataEditView.as_view(),
        name='study_metadata_edit'),

    url(r'^(?P<pk>\d+)/detail$',
        views.StudyMetadataDetailView.as_view(),
        name='study_metadata_detail'),

    url(r'^(?P<pk>\d+)/context/detail$',
        views.StudyContextDetailView.as_view(),
        name='study_context_detail'),

    url(r'^(?P<pk>\d+)/context/edit$',
        views.StudyContextEditView.as_view(),
        name='study_context_edit'),

    url(r'^(?P<pk>\d+)/outcomes/detail$',
        views.StudyOutcomesDetailView.as_view(),
        name='study_outcomes_detail'),

    url(r'^(?P<pk>\d+)/outcomes/edit$',
        views.StudyOutcomesAddView.as_view(),
        name='study_outcomes_edit'),

    url(r'^(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/detail$',
        views.StudyOutcomeDetailView.as_view(),
        name='study_outcome_detail'),

    url(r'^(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/delete$',
        views.StudyOutcomeDeleteView.as_view(),
        name='study_outcome_delete'),

    url(r'^(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/edit$',
        views.StudyOutcomeEditView.as_view(),
        name='study_outcome_edit'),

)


urlpatterns = patterns(

    '',

    url(r'^$',
        views.StudiesView.as_view(),
        name='studies_overview'),

    url(r'^studies/overview/$',
        views.StudiesView.as_view(),
        name='studies_overview'),

    url(r'^studies/my-entries/$',
        views.MyEntriesView.as_view(),
        name='my_entries'),

    url(r'^study/', include(study_urls)),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
