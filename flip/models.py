
from django.db.models import BooleanField
from django.db.models import CharField, URLField, TextField
from django.db.models import DateField, DateTimeField
from django.db.models import ManyToManyField, ForeignKey
from django.db.models import Model


class Study(Model):

    EEA = 'eea'
    REQUESTED_BY_CHOICES = (
        (EEA, 'EEA'),
    )

    YES = 'yes'
    NO = 'no'
    YES_NO_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No'),
    )

    POLICY = 'policy'
    NON_POLICY = 'non_policy'
    PURPOSE_CHOICES = (
        (POLICY, 'Support to policy'),
        (NON_POLICY, 'Non-policy (research, civil initiative, NGOs...'),
    )

    draft = BooleanField(default=True)

    created_on = DateTimeField(auto_now_add=True)

    last_updated = DateTimeField(auto_now_add=True, auto_now=True)

    user_id = CharField(max_length=64, blank=True)

    title = CharField(
        'study title in English',
        max_length=255)

    languages = ManyToManyField(
        'Language',
        verbose_name='language of the study',
        through='StudyLanguage')

    url = URLField(blank=True)

    blossom = CharField(
        'is it a BLOSSOM study?',
        max_length=8,
        choices=YES_NO_CHOICES,
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

    phases_of_policy = ForeignKey(
        'PhasesOfPolicy',
        verbose_name='phases of policy cycle',
        null=True,
        blank=True)

    additional_information_phase = TextField(
        ('additional information about phase of policy cycle and '
         'domain of application'),
        blank=True)

    foresight_approaches = ForeignKey(
        'ForesightApproaches',
        verbose_name='foresight approaches used',
        null=True,
        blank=True)

    stakeholder_participation = BooleanField(
        'stakeholder participation',
        default=False)

    additional_information_stakeholder = TextField(
        'additional information about stakeholder involvement',
        blank=True)

    environmental_themes = ManyToManyField(
        'EnvironmentalTheme',
        verbose_name='environmental themes',
        blank=True)

    geographical_scope = ForeignKey(
        'GeographicalScope',
        verbose_name='geographical scope',
        null=True,
        blank=True)

    countries = ManyToManyField(
        'Country',
        verbose_name='country',
        blank=True)

    def __unicode__(self):
        return self.title


class Language(Model):

    code = CharField(max_length=3, primary_key=True)
    title = CharField(max_length=32)

    def __unicode__(self):
        return self.title


class StudyLanguage(Model):

    language = ForeignKey(
        Language,
        verbose_name='language of the study')
    study = ForeignKey(Study)
    title = CharField(
        'study title in original languge',
        max_length=255)

    def __unicode__(self):
        return self.title


class PhasesOfPolicy(Model):

    title = CharField(max_length=128)

    def __unicode__(self):
        return self.title


class ForesightApproaches(Model):

    title = CharField(max_length=128)

    def __unicode__(self):
        return self.title


class EnvironmentalTheme(Model):

    title = CharField(max_length=128)

    def __unicode__(self):
        return self.title


class GeographicalScope(Model):

    title = CharField(max_length=128)

    def __unicode__(self):
        return self.title


class Country(Model):

    iso = CharField(max_length=2, primary_key=True)
    name = CharField(max_length=128)

    def __unicode__(self):
        return self.name
