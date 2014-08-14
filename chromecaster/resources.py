#!/usr/bin/env python

from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops

from models import Media, Playlist


class MediaResource(Resource):
    document = Media


class PlaylistResource(Resource):
    document = Playlist
    related_resources = {
        'media': MediaResource,
    }
    filters = {
        'title': [ops.Exact, ops.Startswith],
        'author_id': [ops.Exact],
    }
    rename_fields = {
        'author': 'author_id',
    }
