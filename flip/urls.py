from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from flip import views


admin.autodiscover()


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
        views.StudyOutcomesHomeView.as_view(),
        name='study_outcomes'),

    url(r'^study/(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/detail$',
        views.StudyOutcomesView.as_view(),
        name='study_outcomes_detail'),

    url(r'^study/(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/delete$',
        views.StudyOutcomesDeleteView.as_view(),
        name='study_outcomes_delete'),

    url(r'^study/(?P<pk>\d+)/outcomes/(?P<outcome_pk>\d+)/edit$',
        views.StudyOutcomesEditView.as_view(),
        name='study_outcomes_edit'),

    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
