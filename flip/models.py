
from django.db.models import BooleanField, IntegerField
from django.db.models import CharField, URLField, TextField, FileField
from django.db.models import DateField, DateTimeField
from django.db.models import ManyToManyField, ForeignKey
from django.db.models import Model

from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Study(Model):

    EEA = 'eea'
    OTHER = 'other'
    REQUESTED_BY_CHOICES = (
        (EEA, 'EEA'),
        (OTHER, 'Other'),
    )

    YES = 1
    NO = 0
    YES_NO_CHOICES = (
        ('', '----'),
        (YES, 'Yes'),
        (NO, 'No'),
    )

    POLICY = 'policy'
    NON_POLICY = 'non_policy'
    PURPOSE_CHOICES = (
        (POLICY, 'Support to policy'),
        (NON_POLICY, 'Non-policy (research, civil initiative, NGOs...'),
    )

    ACTIVITY = 'activity'
    ASSESSMENT = 'assessment'
    TYPE_CHOICES = (
        (ACTIVITY, 'Forward looking activity'),
        (ASSESSMENT, 'Assessment'),
    )

    BLOSSOM_CHOICES = (
        (YES, 'BLOSSOM study'),
        (NO, 'other study'),
    )

    draft = BooleanField(default=True)

    created_on = DateTimeField(auto_now_add=True)

    last_updated = DateTimeField(auto_now_add=True, auto_now=True)

    user_id = CharField(max_length=64, blank=True)

    title = CharField(
        'title in English',
        max_length=255)

    languages = ManyToManyField(
        'Language',
        verbose_name='language of the study',
        through='StudyLanguage')

    url = URLField(blank=True)

    study_type = CharField(
        'I want to add a new',
        choices=TYPE_CHOICES,
        max_length=128,
        null=True,
    )

    blossom = IntegerField(
        'Approach to assessment',
        choices=BLOSSOM_CHOICES,
        default=NO,
    )

    requested_by = CharField(
        'who requested the study?',
        max_length=64,
        choices=REQUESTED_BY_CHOICES,
        blank=True
    )

    start_date = DateField('start date', null=True, blank=True)

    end_date = DateField('end date')

    lead_author = TextField('lead author')

    other = TextField(
        'other organisations/authors or contact persons',
        blank=True
    )

    purpose_and_target = CharField(
        'purpose and target audience',
        max_length=128,
        choices=PURPOSE_CHOICES,
        blank=True,
    )

    additional_information = TextField(
        'additional information',
        blank=True)

    phase_of_policy = ForeignKey(
        'PhasesOfPolicy',
        verbose_name='phases of policy cycle',
        null=True,
        blank=True)

    additional_information_phase = TextField(
        ('additional information about the application'),
        blank=True)

    foresight_approaches = ManyToManyField(
        'ForesightApproaches',
        verbose_name='foresight approaches used')

    additional_information_foresight = TextField(
        'additional information',
        blank=True)

    stakeholder_participation = BooleanField(
        'stakeholder participation',
        default=False)

    additional_information_stakeholder = TextField(
        'additional information about stakeholder involvement',
        blank=True)

    environmental_themes = ManyToManyField(
        'common.EnvironmentalTheme',
        verbose_name='topics',
        blank=True)

    geographical_scope = ForeignKey(
        'common.GeographicalScope',
        verbose_name='geographical scope',
        null=True,
        blank=True)

    countries = ManyToManyField(
        'common.Country',
        verbose_name='countries',
        blank=True)

    def __unicode__(self):
        return self.title


class Outcome(Model):

    study = ForeignKey(Study, related_name='outcomes')

    type_of_outcome = ForeignKey(
        'TypeOfOutcome',
        verbose_name='type of output',
        null=True,
        blank=True)

    document_title = CharField('title', max_length=255)

    text = TextField('text', null=True, blank=True)

    file_id = FileField(upload_to='outcomes', max_length=256, null=True,
                        blank=True, default='', verbose_name='File')

    def __unicode__(self):
        return self.document_title


class Language(Model):

    code = CharField(max_length=3, primary_key=True)
    title = CharField(max_length=32)

    def __unicode__(self):
        return self.title


class StudyLanguage(Model):

    language = ForeignKey(Language, verbose_name='language of the study')

    study = ForeignKey(Study)

    title = CharField('title in original language', max_length=255)

    def __unicode__(self):
        return self.title


class PhasesOfPolicy(Model):

    title = CharField(max_length=128)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return self.title


class ForesightApproaches(Model):

    title = CharField(max_length=128)

    class Meta:
        ordering = ('-pk',)

    def __unicode__(self):
        return self.title


class TypeOfOutcome(Model):
    TYPE_CHOICES = (
        ('all', 'All'),
        (Study.ACTIVITY, 'Forward looking activity'),
        (Study.ASSESSMENT, 'Assessment'),
    )

    title = CharField(max_length=256)
    blossom = BooleanField(default=False)
    doc_type = CharField(
        'Type',
        choices=TYPE_CHOICES,
        max_length=128,
        null=True,
        default = 'all'
    )

    class Meta:
        ordering = ('pk',)

    def __unicode__(self):
        return self.title


@receiver(pre_delete, sender=Outcome)
def outcome_delete_file(sender, instance, **kwargs):
    instance.file_id.delete(save=False)
