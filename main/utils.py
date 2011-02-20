# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify

def to_h_system(word):
    h_system = {u'ĉ':u'ch', u'Ĉ':u'Ch', u'ĝ':u'gh', u'Ĝ':u'Gh', u'ĥ':u'hh',
                u'Ĥ':u'Hh', u'ĵ':u'jh', u'Ĵ':u'Jh', u'ŝ':u'sh', u'Ŝ':u'Sh',
                u'ŭ':u'u', u'Ŭ':u'U'}
    output = []
    for letter in list(word):
        if letter in h_system.keys():
            output.append(h_system[letter])
        else:
            output.append(letter)
    return ''.join(output)

def eo_slugify(text):
    return slugify(to_h_system(text))
