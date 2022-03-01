from django.contrib.postgres import fields
import django_filters
from .models import *
from django_filters import CharFilter,ChoiceFilter

class PdfFilter(django_filters.FilterSet):

    std_choices = (
        ('BURAK İLHAN','Burak İlhan'),
        ('MERT TOPRAK','Mert Toprak'),
        ('ALİ EKEN','Ali Eken')
    )

    lesson_choices = (
        ('ARAŞTIRMA PROBLEMLERİ','Araştırma Problemleri'),
        ('BİTİRME PROJESİ','Bitirme Projesi')
    )

    term_choices = (
        ('2020-2021 Bahar','2020-2021 Bahar'),
        ('2021-2022 Güz','2021-2022 Güz')
    )

    std_query = django_filters.ChoiceFilter(field_name='student',label = 'Student', choices =std_choices)
    lesson_query = django_filters.ChoiceFilter(field_name='lesson',label = 'Lesson', choices =lesson_choices)
    term_query = django_filters.ChoiceFilter(field_name='season',label = 'Term', choices =term_choices)

    note = CharFilter(field_name='keywords', lookup_expr='icontains')
    
    class Meta:
        model = Pdf
        fields = ['title']
