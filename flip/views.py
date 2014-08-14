
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404
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


class StudyMetadataDetailView(LoginRequiredMixin,
                              generic.DetailView):

    model = models.Study
    template_name = 'study/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = {'form': forms.StudyMetadataForm(),
                   'selected_tab': 0}
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
        context = {'selected_tab': 0}
        context.update(kwargs)
        return super(StudyMetadataEditView, self).get_context_data(**context)

    def get_success_url(self):
        return reverse('study_metadata_edit',
                       kwargs={'pk': self.object.pk})


class StudyContextDetailView(LoginRequiredMixin,
                             generic.DetailView):

    model = models.Study
    template_name = 'study/context_detail.html'

    def get_context_data(self, **kwargs):
        context = {'form': forms.StudyContextForm(),
                   'selected_tab': 1}
        context.update(kwargs)
        return super(StudyContextDetailView, self).get_context_data(**context)


class StudyContextEditView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyBlossomRequiredMixin,
                           SuccessMessageMixin,
                           generic.UpdateView):

    model = models.Study
    form_class = forms.StudyContextForm
    template_name = 'study/context_edit.html'
    success_message = 'The study was successfully updated'

    def get_success_url(self):
        return reverse('study_context_detail',
                       kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = {'form': forms.StudyContextForm(),
                   'selected_tab': 1}
        context.update(kwargs)
        return super(StudyContextEditView, self).get_context_data(**context)


class StudyOutcomesDetailView(LoginRequiredMixin,
                              generic.DetailView):

    model = models.Study
    template_name = 'study/outcomes_detail.html'

    def get_object(self):
        return get_object_or_404(models.Study, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = {'form': forms.OutcomeForm(study=self.object),
                   'selected_tab': 2}
        context.update(kwargs)
        return super(StudyOutcomesDetailView, self).get_context_data(**context)


class StudyOutcomesAddView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyBlossomRequiredMixin,
                           SuccessMessageMixin,
                           generic.CreateView):

    model = models.Outcome
    form_class = forms.OutcomeForm
    template_name = 'study/outcomes_detail.html'

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
        return reverse('study_outcomes_detail', kwargs={'pk': self.study.pk})

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
        context = {'study': self.study}
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
        context = {'study': self.study}
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

    def get_queryset(self):
        queryset = models.Study.objects.all()
        blossom = self.request.GET.get('blossom')
        phase_of_policy = self.request.GET.get('phase_of_policy')
        foresight_approaches = self.request.GET.getlist('foresight_approaches')
        if blossom:
            queryset = queryset.filter(blossom=blossom)
            if phase_of_policy:
                queryset = queryset.filter(phase_of_policy=phase_of_policy)
            if foresight_approaches:
                queryset = queryset.filter(
                    foresight_approaches__in=foresight_approaches).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context['filter_form'] = forms.FilterForm(self.request.GET)
        filter_params = ['blossom', 'phase_of_policy', 'foresight_approaches']
        context['filtering'] = False
        for filter_param in filter_params:
            if self.request.GET.get(filter_param):
                context['filtering'] = True
                break
        context.update(kwargs)
        return super(StudiesView, self).get_context_data(**context)


class MyEntriesView(LoginRequiredMixin,
                    generic.ListView):

    model = models.Study
    template_name = 'my_entries.html'

    def get_queryset(self):
        queryset = models.Study.objects.all()
        blossom = self.request.GET.get('blossom')
        phase_of_policy = self.request.GET.get('phase_of_policy')
        foresight_approaches = self.request.GET.getlist('foresight_approaches')
        queryset = queryset.filter(user_id=self.request.user_id)
        if blossom:
            queryset = queryset.filter(blossom=blossom)
            if phase_of_policy:
                queryset = queryset.filter(phase_of_policy=phase_of_policy)
            if foresight_approaches:
                queryset = queryset.filter(
                    foresight_approaches__in=foresight_approaches).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context['filter_form'] = forms.FilterForm(self.request.GET)
        filter_params = ['blossom', 'phase_of_policy', 'foresight_approaches']
        context['filtering'] = False
        for filter_param in filter_params:
            if self.request.GET.get(filter_param):
                context['filtering'] = True
        context.update(kwargs)
        return super(MyEntriesView, self).get_context_data(**context)


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
