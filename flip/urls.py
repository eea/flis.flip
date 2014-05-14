from django.conf.urls import patterns, include, url
from django.contrib import admin
from flip import views


admin.autodiscover()


urlpatterns = patterns(

    '',

    url(r'^$',
        views.HomeView.as_view(),
        name='studies_overview'),

    url(r'^study/new/$',
        views.StudyMetadataAddView.as_view(),
        name='study_metadata_edit'),

    url(r'^study/(?P<pk>\d+)/edit$',
        views.StudyMetadataEditView.as_view(),
        name='study_metadata_edit'),

    url(r'^study/(?P<pk>\d+)/context/edit$',
        views.StudyContextEditView.as_view(),
        name='study_context_edit'),

    url(r'^study/(?P<pk>\d+)/outcomes/edit$',
        views.StudyOutcomesEditView.as_view(),
        name='study_outcomes_edit'),

    url(r'^admin/', include(admin.site.urls)),

)
