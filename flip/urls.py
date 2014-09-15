from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

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

    url(r'^phases_of_policy/(?P<pk>\d+)/delete$',
        views.SettingsPhasesOfPolicyDeleteView.as_view(),
        name='phases_of_policy_delete'),

    url(r'^foresight_approaches/$',
        views.SettingsForesightApproachesView.as_view(),
        name='foresight_approaches'),

    url(r'^foresight_approaches/new$',
        views.SettingsForesightApproachesAddView.as_view(),
        name='foresight_approaches_edit'),

    url(r'^foresight_approaches/(?P<pk>\d+)/edit$',
        views.SettingsForesightApproachesEditView.as_view(),
        name='foresight_approaches_edit'),

    url(r'^foresight_approaches/(?P<pk>\d+)/delete$',
        views.SettingsForesightApproachesDeleteView.as_view(),
        name='foresight_approaches_delete'),

    url(r'^environmental_themes/$',
        views.SettingsEnvironmentalThemesView.as_view(),
        name='environmental_themes'),

    url(r'^environmental_themes/new$',
        views.SettingsEnvironmentalThemesAddView.as_view(),
        name='environmental_themes_edit'),

    url(r'^environmental_themes/(?P<pk>\d+)/edit$',
        views.SettingsEnvironmentalThemesEditView.as_view(),
        name='environmental_themes_edit'),

    url(r'^environmental_themes/(?P<pk>\d+)/delete$',
        views.SettingsEnvironmentalThemesDeleteView.as_view(),
        name='environmental_themes_delete'),

    url(r'^geographical_scopes/$',
        views.SettingsGeographicalScopesView.as_view(),
        name='geographical_scopes'),

    url(r'^geographical_scopes/new$',
        views.SettingsGeographicalScopesAddView.as_view(),
        name='geographical_scopes_edit'),

    url(r'^geographical_scopes/(?P<pk>\d+)/edit$',
        views.SettingsGeographicalScopesEditView.as_view(),
        name='geographical_scopes_edit'),

    url(r'^geographical_scopes/(?P<pk>\d+)/delete$',
        views.SettingsGeographicalScopesDeleteView.as_view(),
        name='geographical_scopes_delete'),

    url(r'^outcomes/$',
        views.SettingsOutcomesView.as_view(),
        name='outcomes'),

    url(r'^outcomes/new$',
        views.SettingsOutcomesAddView.as_view(),
        name='outcomes_edit'),

    url(r'^outcomes/(?P<pk>\d+)/edit$',
        views.SettingsOutcomesEditView.as_view(),
        name='outcomes_edit'),

    url(r'^outcomes/(?P<pk>\d+)/delete$',
        views.SettingsOutcomesDeleteView.as_view(),
        name='outcomes_delete'),

    url(r'^topics/$',
        views.SettingsTopicsView.as_view(),
        name='topics'),

    url(r'^topics/new$',
        views.SettingsTopicAddView.as_view(),
        name='topics_add'),

    url(r'^topics/(?P<pk>\d+)/edit$',
        views.SettingsTopicEditView.as_view(),
        name='topics_edit'),

    url(r'^topics/(?P<pk>\d+)/delete$',
        views.SettingsTopicDeleteView.as_view(),
        name='topics_delete'),

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

    url(r'^(?P<pk>\d+)/delete$',
        views.StudyDeleteView.as_view(),
        name='study_delete'),

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
        TemplateView.as_view(template_name="home.html"),
        name='home_view'),

    url(r'^studies/overview/$',
        views.StudiesView.as_view(),
        name='studies_overview'),

    url(r'^studies/', include(study_urls)),

    url(r'^settings/', include(settings_urls, namespace='settings')),

    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
