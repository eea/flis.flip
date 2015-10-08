from django.views.generic import ListView, DetailView
from flip.models import Study


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

