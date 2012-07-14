# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter(name='eo_date')
def eo_date(date):
    date_string = date.strftime('%A, la %e-a de %B %Y')

    days = ((u'Monday', u'Lundo'), (u'Tuesday', u'Mardo'),
            (u'Wednesday', u'Merkredo'), (u'Thurday', u'Ĵaŭdo'),
            (u'Friday', u'Vendredo'), (u'Saturday', u'Sabato'),
            (u'Sunday', u'Dimanĉo'))

    # decided to do Esperanto months lower case, since that's what Vikipedio does
    months = ((u'January', u'januaro'), (u'February', u'februaro'),
              (u'March', u'marto'), (u'April', u'aprilo'), (u'May', u'majo'),
              (u'June', u'junio'), (u'July', u'julio'), (u'August', u'aŭgusto'),
              (u'September', u'septembro'), (u'October', u'oktobro'),
              (u'November', u'novembro'), (u'December', u'decembro'))

    for (english_day, esperanto_day) in days:
        date_string = date_string.replace(english_day, esperanto_day)

    for (english_month, esperanto_month) in months:
        date_string = date_string.replace(english_month, esperanto_month)
        
    return date_string
