import time

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.http import Http404

from flip import forms, models
from auth.views import LoginRequiredMixin, EditPermissionRequiredMixin
from auth.views import AdminPermissionRequiredMixin
from auth.views import is_admin

from flis_metadata.common.models import GeographicalScope

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


class ParametersMixin(object):
    def dispatch(self, request, **kwargs):
        study_type = kwargs.get('study_type', None)
        pk = kwargs.get('pk', None)

        if study_type:
            if not study_type in dict(models.Study.TYPE_CHOICES).keys():
                raise Http404
            self.study_type = study_type
        if pk:
            self.pk = pk
        return super(ParametersMixin, self).dispatch(request, **kwargs)


class StudyMetadataAddView(LoginRequiredMixin,
                           EditPermissionRequiredMixin,
                           StudyLanguageFormMixin,
                           SuccessMessageMixin,
                           ParametersMixin,
                           generic.CreateView):

    model = models.Study
    form_class = forms.StudyMetadataForm
    template_name = 'study/study_add.html'
    success_message = 'The study was successfully updated'

    def get_success_url(self):
        kwargs = {'pk': self.object.pk,
                  'study_type': self.object.study_type}
        return reverse('study_metadata_detail', kwargs=kwargs)

    def get_context_data(self, **kwargs):
        self.request.session['first_time_edit'] = True
        require_country = [str(scope.id) for scope in GeographicalScope.
            objects.filter(require_country=True)]
        context = {'cancel_url': reverse('studies_overview'),
                   'require_country': require_country}

        if hasattr(self, 'study_type'):
            context['study_type'] = self.study_type

        context.update(kwargs)
        return super(StudyMetadataAddView, self).get_context_data(**context)


class StudyMetadataDetailView(LoginRequiredMixin,
                              ParametersMixin,
                              generic.DetailView):

    model = models.Study
    template_name = 'study/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'form': forms.StudyMetadataForm(),
            'show_submit_create': True,
        }
        if 'first_time_edit' in self.request.session:
            context['open_popup'] = True
            self.request.session.clear()
        context.update(kwargs)
        return super(StudyMetadataDetailView, self).get_context_data(**context)


class StudyOutcomesSectionView(LoginRequiredMixin,
                               generic.DetailView):
    model = models.Study
    template_name = 'study/outcomes_section.html'


class StudyMetadataEditView(LoginRequiredMixin,
                            EditPermissionRequiredMixin,
                            StudyLanguageFormMixin,
                            SuccessMessageMixin,
                            ParametersMixin,
                            generic.UpdateView):

    model = models.Study
    form_class = forms.StudyMetadataForm
    template_name = 'study/study_edit.html'
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
        require_country = [str(scope.id) for scope in GeographicalScope.
            objects.filter(require_country=True)]
        context = {'cancel_url': reverse('study_metadata_detail',
                                         kwargs={'pk': self.object.pk}),
                   'edit_mode': True,
                   'require_country': require_country}
        context.update(kwargs)
        return super(StudyMetadataEditView, self).get_context_data(**context)

    def get_success_url(self):
        kwargs = {'pk': self.object.pk}
        if hasattr(self, 'study_type'):
            kwargs['study_type'] = self.study_type
        return reverse('study_metadata_detail', kwargs=kwargs)


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

    def post(self, request, pk, study_type):
        study = get_object_or_404(models.Study, pk=pk)
        study.draft = not study.draft
        study.save()
        return redirect(reverse('study_metadata_detail',
                                kwargs={'pk': pk,
                                        'study_type': study_type}))


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

    def get_form_kwargs(self):
        kwargs = super(StudyOutcomesAddView, self).get_form_kwargs()
        kwargs['study'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return reverse('study_outcomes_detail',
                       kwargs={'pk': self.get_object().pk})

    def get_success_message(self, cleaned_data):
        return u'{document_title} was successfully added'.format(
            **cleaned_data)


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
                           SuccessMessageMixin,
                           generic.UpdateView):

    model = models.Outcome
    form_class = forms.OutcomeForm
    pk_url_kwarg = 'outcome_pk'
    template_name = 'study/outcome_edit.html'

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
        return reverse('study_metadata_detail', kwargs={'pk': self.study.pk})

    def get_success_message(self, cleaned_data):
        return u'{document_title} was successfully updated'.format(
            **cleaned_data)


class StudyOutcomeEditModalView(StudyOutcomeEditView):
    template_name = 'study/outcome_edit_form.html'

    def get_success_url(self):
        return reverse('study_outcomes_detail', kwargs={'pk': self.study.pk})


class UserEntriesView(LoginRequiredMixin,
                  generic.ListView):

    model = models.Study
    template_name = 'user_entries.html'

    def get(self, request, *args, **kwargs):
        return super(UserEntriesView, self).get(request, args, kwargs)

    def get_queryset(self):
        queryset = models.Study.objects.filter(user_id=self.request.user_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'filter_form': forms.FilterForm(self.request.GET),
        }
        context.update(kwargs)
        return super(UserEntriesView, self).get_context_data(**context)


class StudiesView(LoginRequiredMixin,
                  ParametersMixin,
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

        if hasattr(self, 'study_type'):
            queryset = queryset.filter(study_type=self.study_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = {
            'filter_form': forms.FilterForm(self.request.GET),
            'filtering': any([self.blossom,
                             self.phase_of_policy,
                             self.foresight_approaches,
                             self.my_entries])
        }
        if hasattr(self, 'study_type'):
            context['study_type'] = self.study_type
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
