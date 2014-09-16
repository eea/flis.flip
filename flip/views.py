import time

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from flip import forms, models
from auth.views import LoginRequiredMixin, EditPermissionRequiredMixin
from auth.views import AdminPermissionRequiredMixin
from auth.views import is_admin


class StudyBlossomRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        study = self.get_object()
        if not study.blossom:
            raise Http404
        return super(StudyBlossomRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class StudyLanguageFormMixin(object):

    def get_context_data(self, *args, **kwargs):
        data = super(StudyLanguageFormMixin, self) \
            .get_context_data(*args, **kwargs)
        data['formset'] = self.get_formset(self.request.POST)
        return data

    def get_formset(self, data=None):
        max_num = models.Language.objects.count()
        extra = 0 if self.object else 1
        StudyLanguageInlineFormSet = inlineformset_factory(
            models.Study, models.StudyLanguage,
            formset=forms.BaseStudyLanguageInlineFormSet,
            fields=('language', 'title'),
            extra=extra, max_num=max_num, validate_max=True, can_delete=True)

        if data:
            return StudyLanguageInlineFormSet(data, instance=self.object)
        else:
            return StudyLanguageInlineFormSet(instance=self.object)

    def get_form_kwargs(self):
        kwargs = super(StudyLanguageFormMixin, self).get_form_kwargs()
        kwargs['formset'] = self.get_formset(self.request.POST)
        kwargs['user_id'] = self.request.user_id
        return kwargs


class StudyMetadataAddView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyLanguageFormMixin,
                           SuccessMessageMixin,
                           generic.CreateView):

    model = models.Study
    form_class = forms.StudyMetadataForm
    template_name = 'study/metadata_edit.html'
    success_message = 'The study was successfully updated'

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = {'cancel_url': reverse('studies_overview')}
        context.update(kwargs)
        return super(StudyMetadataAddView, self).get_context_data(**context)


class StudyMetadataDetailView(LoginRequiredMixin,
                              generic.DetailView):

    model = models.Study
    template_name = 'study/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'form': forms.StudyMetadataForm(),
            'context_form': forms.StudyContextForm(),
        }
        context.update(kwargs)
        return super(StudyMetadataDetailView, self).get_context_data(**context)


class StudyMetadataEditView(LoginRequiredMixin,
                            EditPermissionRequiredMixin,
                            StudyLanguageFormMixin,
                            SuccessMessageMixin,
                            generic.UpdateView):

    model = models.Study
    form_class = forms.StudyMetadataForm
    template_name = 'study/metadata_edit.html'
    success_message = 'The study was successfully updated'

    def get_queryset(self, queryset=None):
        if is_admin(self.request):
            return self.model._default_manager.all()._clone()
        else:
            return (
                self.model._default_manager
                .filter(user_id=self.request.user_id)
                ._clone()
            )

    def get_context_data(self, **kwargs):
        context = {'cancel_url': reverse('study_metadata_detail',
                                         kwargs={'pk': self.object.pk})}
        context.update(kwargs)
        return super(StudyMetadataEditView, self).get_context_data(**context)

    def get_success_url(self):
        return reverse('study_metadata_detail',
                       kwargs={'pk': self.object.pk})


class StudyDeleteView(LoginRequiredMixin,
                      EditPermissionRequiredMixin,
                      generic.DeleteView):

    model = models.Study
    template_name = 'study/study_confirm_delete.html'

    def get_success_url(self):
        return reverse('studies_overview')


class StudyStatusEditView(LoginRequiredMixin,
                          EditPermissionRequiredMixin,
                          generic.View):

    def post(self, request, pk):
        study = get_object_or_404(models.Study, pk=pk)
        study.draft = not study.draft
        study.save()
        return redirect(reverse('study_metadata_detail',
                                kwargs={'pk': pk}))


class StudyContextDetailView(LoginRequiredMixin,
                             generic.DetailView):

    model = models.Study
    template_name = 'study/context_detail.html'

    def get_context_data(self, **kwargs):
        context = {'form': forms.StudyContextForm()}
        context.update(kwargs)
        return super(StudyContextDetailView, self).get_context_data(**context)


class StudyContextEditView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyBlossomRequiredMixin,
                           SuccessMessageMixin,
                           generic.UpdateView):

    model = models.Study
    form_class = forms.StudyContextForm
    template_name = 'study/context_edit_form.html'
    success_message = 'The study was successfully updated'

    def get_success_url(self):
        return reverse('study_context_detail',
                       kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = {'form': forms.StudyContextForm(),
                   'cancel_url': reverse('study_context_detail',
                                         kwargs={'pk': self.object.pk})}
        context.update(kwargs)
        return super(StudyContextEditView, self).get_context_data(**context)


class StudyOutcomesDetailView(LoginRequiredMixin,
                              generic.DetailView):

    model = models.Study
    template_name = 'study/outcomes_detail.html'

    def get_object(self):
        return get_object_or_404(models.Study, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = {'form': forms.OutcomeForm(study=self.object)}
        context.update(kwargs)
        return super(StudyOutcomesDetailView, self).get_context_data(**context)


class StudyOutcomesAddView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyBlossomRequiredMixin,
                           SuccessMessageMixin,
                           generic.CreateView):

    model = models.Outcome
    form_class = forms.OutcomeForm
    template_name = 'study/outcome_add_form.html'

    def get_object(self):
        if getattr(self, 'study', None):
            return self.study
        if is_admin(self.request):
            study = get_object_or_404(models.Study, pk=self.kwargs['pk'])
        else:
            study = get_object_or_404(models.Study, pk=self.kwargs['pk'],
                                      user_id=self.request.user_id)

        study = get_object_or_404(models.Study, pk=self.kwargs['pk'])
        self.study = study
        return study

    def get_context_data(self, **kwargs):
        kwargs = super(StudyOutcomesAddView, self).get_context_data(**kwargs)
        kwargs['study'] = kwargs['object'] = self.study
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(StudyOutcomesAddView, self).get_form_kwargs()
        kwargs['study'] = self.study
        return kwargs

    def get_success_url(self):
        return reverse('study_outcomes_detail', kwargs={'pk': self.study.pk})

    def get_success_message(self, cleaned_data):
        return '{document_title} was successfully added'.format(**cleaned_data)


class StudyOutcomeDeleteView(LoginRequiredMixin,
                             EditPermissionRequiredMixin,
                             generic.DeleteView):

    model = models.Outcome
    pk_url_kwarg = 'outcome_pk'
    template_name = 'study/outcome_confirm_delete.html'

    def dispatch(self, request, pk, outcome_pk):
        self.study = get_object_or_404(models.Study, pk=pk)
        return super(StudyOutcomeDeleteView, self).dispatch(request, pk)

    def get_queryset(self, queryset=None):
        if is_admin(self.request):
            return self.model._default_manager.all()._clone()
        else:
            return (
                self.model._default_manager
                .filter(study__user_id=self.request.user_id)
                ._clone()
            )

    def get_success_url(self):
        return reverse('study_metadata_detail', kwargs={'pk': self.study.pk})

    def get_context_data(self, **kwargs):
        context = {'study': self.study}
        context.update(kwargs)
        return super(StudyOutcomeDeleteView, self).get_context_data(**context)


class StudyOutcomeDetailView(LoginRequiredMixin,
                             generic.DetailView):

    model = models.Outcome
    pk_url_kwarg = 'outcome_pk'
    template_name = 'study/outcome_detail.html'

    def dispatch(self, request, pk, outcome_pk):
        self.study = get_object_or_404(models.Study, pk=pk)
        return super(StudyOutcomeDetailView, self).dispatch(request, pk)

    def get_context_data(self, **kwargs):
        context = {'study': self.study,
                   'back_url': reverse('study_metadata_detail',
                                       kwargs={'pk': self.study.pk})}
        context.update(kwargs)
        return super(StudyOutcomeDetailView, self).get_context_data(**context)


class StudyOutcomeEditView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           generic.UpdateView):

    model = models.Outcome
    form_class = forms.OutcomeForm
    pk_url_kwarg = 'outcome_pk'
    template_name = 'study/outcome_edit.html'
    success_message = 'Outcome was successfully update'

    def dispatch(self, request, pk, outcome_pk):
        self.study = get_object_or_404(models.Study, pk=pk)
        return super(StudyOutcomeEditView, self).dispatch(request, pk)

    def get_queryset(self, queryset=None):
        if is_admin(self.request):
            return self.model._default_manager.all()._clone()
        else:
            return (
                self.model._default_manager
                .filter(study__user_id=self.request.user_id)
                ._clone()
            )

    def get_context_data(self, **kwargs):
        context = {'study': self.study,
                   'cancel_url': reverse('study_outcome_detail',
                                         kwargs={'pk': self.study.pk,
                                                 'outcome_pk': self.object.pk})}
        context.update(kwargs)
        return super(StudyOutcomeEditView, self).get_context_data(**context)

    def get_form_kwargs(self):
        kwargs = super(StudyOutcomeEditView, self).get_form_kwargs()
        kwargs['study'] = self.study
        return kwargs

    def get_success_url(self):
        return reverse('study_outcomes_detail', kwargs={'pk': self.study.pk})


class StudiesView(LoginRequiredMixin,
                  generic.ListView):

    model = models.Study
    template_name = 'studies_overview.html'

    def get(self, request, *args, **kwargs):
        request.session['last_viewed'] = time.time()
        return super(StudiesView, self).get(request, args, kwargs)

    def get_queryset(self):
        self.blossom = self.request.GET.get('blossom')
        self.phase_of_policy = self.request.GET.get('phase_of_policy')
        self.foresight_approaches = self.request.GET.getlist(
            'foresight_approaches')
        self.my_entries = self.request.GET.get('my_entries')

        queryset = models.Study.objects.all()
        if self.my_entries:
            queryset = queryset.filter(user_id=self.request.user_id)

        if self.blossom:
            queryset = queryset.filter(blossom=self.blossom)
            if self.phase_of_policy:
                queryset = queryset.filter(phase_of_policy=self.phase_of_policy)
            if self.foresight_approaches:
                queryset = queryset.filter(
                    foresight_approaches__in=self.foresight_approaches
                ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'filter_form': forms.FilterForm(self.request.GET),
            'filtering': any([self.blossom,
                             self.phase_of_policy,
                             self.foresight_approaches,
                             self.my_entries])
        }
        context.update(kwargs)
        return super(StudiesView, self).get_context_data(**context)


class SettingsPhasesOfPolicyView(LoginRequiredMixin,
                                 AdminPermissionRequiredMixin,
                                 generic.ListView):

    model = models.PhasesOfPolicy
    template_name = 'settings/policy.html'


class SettingsPhasesOfPolicyAddView(LoginRequiredMixin,
                                    AdminPermissionRequiredMixin,
                                    SuccessMessageMixin,
                                    generic.CreateView):

    model = models.PhasesOfPolicy
    template_name = 'settings/policy_edit.html'
    success_message = 'Policy added successfully'

    def get_success_url(self):
        return reverse('settings:phases_of_policy')


class SettingsPhasesOfPolicyEditView(LoginRequiredMixin,
                                     AdminPermissionRequiredMixin,
                                     SuccessMessageMixin,
                                     generic.UpdateView):

    model = models.PhasesOfPolicy
    template_name = 'settings/policy_edit.html'
    success_message = 'Policy updated successfully'

    def get_success_url(self):
        return reverse('settings:phases_of_policy')


class SettingsPhasesOfPolicyDeleteView(LoginRequiredMixin,
                                       AdminPermissionRequiredMixin,
                                       generic.DeleteView):

    model = models.PhasesOfPolicy
    template_name = 'settings/policy_confirm_delete.html'

    def get_success_url(self):
        return reverse('settings:phases_of_policy')


class SettingsForesightApproachesView(LoginRequiredMixin,
                                      AdminPermissionRequiredMixin,
                                      generic.ListView):

    model = models.ForesightApproaches
    template_name = 'settings/foresight_approaches.html'


class SettingsForesightApproachesAddView(LoginRequiredMixin,
                                         AdminPermissionRequiredMixin,
                                         SuccessMessageMixin,
                                         generic.CreateView):

    model = models.ForesightApproaches
    template_name = 'settings/foresight_approaches_edit.html'
    success_message = 'Approach updated successfully'

    def get_success_url(self):
        return reverse('settings:foresight_approaches')


class SettingsForesightApproachesEditView(LoginRequiredMixin,
                                          AdminPermissionRequiredMixin,
                                          SuccessMessageMixin,
                                          generic.UpdateView):

    model = models.ForesightApproaches
    template_name = 'settings/foresight_approaches_edit.html'
    success_message = 'Approach updated successfully'

    def get_success_url(self):
        return reverse('settings:foresight_approaches')


class SettingsForesightApproachesDeleteView(LoginRequiredMixin,
                                            AdminPermissionRequiredMixin,
                                            generic.DeleteView):

    model = models.ForesightApproaches
    template_name = 'settings/foresight_approaches_confirm.html'

    def get_success_url(self):
        return reverse('settings:foresight_approaches')


class SettingsEnvironmentalThemesView(LoginRequiredMixin,
                                      AdminPermissionRequiredMixin,
                                      generic.ListView):

    model = models.EnvironmentalTheme
    template_name = 'settings/environmental_themes.html'


class SettingsEnvironmentalThemesAddView(LoginRequiredMixin,
                                         AdminPermissionRequiredMixin,
                                         SuccessMessageMixin,
                                         generic.CreateView):

    model = models.EnvironmentalTheme
    template_name = 'settings/environmental_themes_edit.html'
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('settings:environmental_themes')


class SettingsEnvironmentalThemesEditView(LoginRequiredMixin,
                                          AdminPermissionRequiredMixin,
                                          SuccessMessageMixin,
                                          generic.UpdateView):

    model = models.EnvironmentalTheme
    template_name = 'settings/environmental_themes_edit.html'
    success_message = 'Theme updated successfully'

    def get_success_url(self):
        return reverse('settings:environmental_themes')


class SettingsEnvironmentalThemesDeleteView(LoginRequiredMixin,
                                            AdminPermissionRequiredMixin,
                                            generic.DeleteView):

    model = models.EnvironmentalTheme
    template_name = 'settings/environmental_themes_confirm_delete.html'

    def get_success_url(self):
        return reverse('settings:environmental_themes')


class SettingsGeographicalScopesView(LoginRequiredMixin,
                                     AdminPermissionRequiredMixin,
                                     generic.ListView):

    model = models.GeographicalScope
    template_name = 'settings/geographical_scopes.html'


class SettingsGeographicalScopesAddView(LoginRequiredMixin,
                                        AdminPermissionRequiredMixin,
                                        SuccessMessageMixin,
                                        generic.CreateView):

    model = models.GeographicalScope
    template_name = 'settings/geographical_scopes_edit.html'
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('settings:geographical_scopes')


class SettingsGeographicalScopesEditView(LoginRequiredMixin,
                                         AdminPermissionRequiredMixin,
                                         SuccessMessageMixin,
                                         generic.UpdateView):

    model = models.GeographicalScope
    template_name = 'settings/geographical_scopes_edit.html'
    success_message = 'Scope updated successfully'

    def get_success_url(self):
        return reverse('settings:geographical_scopes')


class SettingsGeographicalScopesDeleteView(LoginRequiredMixin,
                                           AdminPermissionRequiredMixin,
                                           generic.DeleteView):

    model = models.GeographicalScope
    template_name = 'settings/geographical_scopes_confirm_delete.html'

    def get_success_url(self):
        return reverse('settings:geographical_scopes')


class SettingsOutcomesView(LoginRequiredMixin,
                           AdminPermissionRequiredMixin,
                           generic.ListView):

    model = models.TypeOfOutcome
    template_name = 'settings/outcomes.html'


class SettingsOutcomesAddView(LoginRequiredMixin,
                              AdminPermissionRequiredMixin,
                              SuccessMessageMixin,
                              generic.CreateView):

    model = models.TypeOfOutcome
    template_name = 'settings/outcomes_edit.html'
    success_message = 'Outcome updated successfully'

    def get_success_url(self):
        return reverse('settings:outcomes')


class SettingsOutcomesEditView(LoginRequiredMixin,
                               AdminPermissionRequiredMixin,
                               SuccessMessageMixin,
                               generic.UpdateView):

    model = models.TypeOfOutcome
    template_name = 'settings/outcomes_edit.html'
    success_message = 'Outcome updated successfully'

    def get_success_url(self):
        return reverse('settings:outcomes')


class SettingsOutcomesDeleteView(LoginRequiredMixin,
                                 AdminPermissionRequiredMixin,
                                 generic.DeleteView):

    model = models.TypeOfOutcome
    template_name = 'settings/outcomes_confirm_delete.html'

    def get_success_url(self):
        return reverse('settings:outcomes')


class SettingsTopicsView(LoginRequiredMixin,
                         AdminPermissionRequiredMixin,
                         generic.ListView):

    model = models.ContentTopic
    template_name = 'settings/topics.html'


class SettingsTopicAddView(LoginRequiredMixin,
                           AdminPermissionRequiredMixin,
                           SuccessMessageMixin,
                           generic.CreateView):

    model = models.ContentTopic
    template_name = 'settings/topics_edit.html'
    success_message = 'Outcome topic created successfully'

    def get_success_url(self):
        return reverse('settings:topics')


class SettingsTopicEditView(LoginRequiredMixin,
                            AdminPermissionRequiredMixin,
                            SuccessMessageMixin,
                            generic.UpdateView):

    model = models.ContentTopic
    template_name = 'settings/topics_edit.html'
    success_message = 'Outcome topic updated successfully'

    def get_success_url(self):
        return reverse('settings:topics')


class SettingsTopicDeleteView(LoginRequiredMixin,
                              AdminPermissionRequiredMixin,
                              generic.DeleteView):

    model = models.ContentTopic
    template_name = 'settings/topics_confirm_delete.html'

    def get_success_url(self):
        return reverse('settings:topics')
