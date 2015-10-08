from django.views.generic import ListView, DetailView
from flip.models import Study, Outcome, TypeOfOutcome


class StudiesList(ListView):
    model = Study
    template_name = 'public/policy_cycle.html'

    def get_queryset(self):
        return self.model.objects.filter(
            study_type=Study.ACTIVITY, draft=False
        )


class StudiesDetail(DetailView):
    model = Study
    template_name = 'public/study_detail.html'


class AssessmentsList(ListView):
    model = Study
    template_name = 'public/assessments.html'

    def get_queryset(self):
        return self.model.objects.filter(
            study_type=Study.ASSESSMENT, draft=False
        )

    def get_context_data(self, **kwargs):
        context = super(AssessmentsList, self).get_context_data(**kwargs)
        context['outcome_types'] = TypeOfOutcome.objects.all()
        return context


class OutcomesList(ListView):
    model = Outcome
    template_name = 'public/assessments_outcomes.html'

    def get_queryset(self):
        type_of_outcome = int(self.kwargs['outcome'])

        return self.model.objects.filter(type_of_outcome_id=type_of_outcome)

    def get_context_data(self, **kwargs):
        context = super(OutcomesList, self).get_context_data(**kwargs)
        context['type_of_outcome'] = TypeOfOutcome.objects.get(
            id=self.kwargs['outcome']
        )
        return context
