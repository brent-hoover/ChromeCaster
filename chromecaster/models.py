#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import Document, connect, register_connection
from mongoengine.fields import StringField, DecimalField, ListField, DictField
from mongoengine import connect


connect('chromecaster')
register_connection('default', 'chromecaster')


class Media(Document):

    type = StringField()
    file_id = StringField(primary_key=True)
    artist = StringField()
    title = StringField()
    filename = StringField()
    path = StringField()
    album = StringField()
    description = StringField()
    genre = StringField()
    bpm = DecimalField()
    tags = DictField()
    image = StringField()

    def get_collection(self):
        return self._get_collection()
