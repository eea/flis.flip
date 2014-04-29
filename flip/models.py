
from django.db.models import BooleanField
from django.db.models import CharField, URLField, TextField
from django.db.models import DateField, DateTimeField
from django.db.models import ManyToManyField
from django.db.models import Model


class Study(Model):

    EEA = 'eea'
    REQUESTED_BY_CHOICES = (
        (EEA, 'EEA'),
    )

    draft = BooleanField(default=True)

    created_on = DateTimeField(auto_now_add=True)

    last_updated = DateTimeField(auto_now_add=True, auto_now=True)

    user_id = CharField(max_length=64, blank=True)

    title = CharField(
        'study title in English',
        max_length=255)

    language = ManyToManyField(
        'Language',
        verbose_name='language of the study')

    title_original = CharField(
        'study title in original language',
        max_length=255)

    url = URLField(blank=True)

    blossom = BooleanField(
        'is it a BLOSSOM study?',
        default=False)

    requested_by = CharField(
        'who requested the study?',
        max_length=64,
        choices=REQUESTED_BY_CHOICES,
        blank=True
    )

    start_date = DateField('start date', blank=True)

    end_date = DateField('end date')

    lead_author = TextField('lead author')

    other = TextField(
        'other organisations/authors or contact persons',
         blank=True)

    def __unicode__(self):
        return self.title


class Language(Model):

    code = CharField(max_length=3, primary_key=True)
    title = CharField(max_length=32)

    def __unicode__(self):
        return self.title
