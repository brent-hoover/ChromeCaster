#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import Document, register_connection, EmbeddedDocument, fields

register_connection('default', 'chromecaster')


class Settings(Document):
    setting = fields.StringField(primary_key=True)


class Media(Document):

    type = fields.StringField()
    file_id = fields.StringField(primary_key=True)
    artist = fields.StringField()
    title = fields.StringField()
    filename = fields.StringField()
    path = fields.StringField()
    album = fields.StringField()
    description = fields.StringField()
    genre = fields.StringField()
    bpm = fields.DecimalField()
    tags = fields.DictField()
    image = fields.StringField()

    def get_collection(self):
        return self._get_collection()


class PlayListItem(EmbeddedDocument):
    media_item = fields.ReferenceField('Media')
    sort_order = fields.IntField()


class Playlist(Document):
    name = fields.StringField(primary_key=True)
    playlist_items = fields.ListField(fields.EmbeddedDocumentField(PlayListItem))
