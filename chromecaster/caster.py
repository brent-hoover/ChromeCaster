#!/usr/bin/env python
import os
import sys
import logging
from logging import StreamHandler
from hashlib import sha1
from mutagen.mp3 import EasyMP3 as MP3, HeaderNotFoundError
from mutagen.easymp4 import EasyMP4
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from walkdir import filtered_walk, file_paths
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest import methods

from models import Media
from chromecaster.lib.send_file import send_file_partial
from resources import MediaResource, PlaylistResource


logger = logging.getLogger()
shandler = StreamHandler()
logger.addHandler(shandler)
logger.setLevel(logging.DEBUG)

# CORS allow origin * is not safe for production
cors_headers = {'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE',
                'Access-Control-Allow-Headers': 'Content-Type'}

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)
api = MongoRest(app)
app.config['MONGODB_SETTINGS'] = {'DB': 'chromecaster', 'HOST' : '127.0.0.1', 'PORT': 27017}
db = MongoEngine(app)


def run():
    logger.debug('starting...')
    this_app = config_app(filename='default.py', app_instance=app)
    return this_app


def _get_tags(file_path):
    if '.mp3' in file_path:
        tags = dict()
        try:
            easymp3 = MP3(file_path)
            logger.debug(easymp3.keys())
            tags['title'] = easymp3.get('title', [''])[0]
            tags['artist'] = easymp3.get('artist', [''])[0]
            return tags
        except HeaderNotFoundError, e:
            return dict()
    elif '.mp4' in file_path:
        logger.debug(file_path)
        tags = dict()
        try:
            easymp4 = EasyMP4(file_path)
            logger.debug(easymp4.keys())
            tags['title'] = easymp4.get('title', [''])[0]
            tags['artist'] = easymp4.get('artist', [''])[0]
            return tags
        except HeaderNotFoundError, e:
            return dict()
    else:
        return dict()


def index_content(root_dir, file_types, content_type):
    """ Scan the media directory, creating an index of file properties for display and serving
    """
    logger.debug('indexing')
    hasher = sha1()
    content_dir = os.path.join(root_dir, app.config['CONTENT_DIR'])
    files = file_paths(filtered_walk(content_dir, included_files=file_types, ))
    for contentfile in files:
        rel_path = os.path.relpath(contentfile, root_dir)
        filepath = os.path.join(root_dir, rel_path)
        filename = os.path.split(contentfile)[1]
        local_path = os.path.relpath(filepath, root_dir)
        if os.path.exists(os.path.join(filepath, 'folder.jpg')):
            img = os.path.join(filepath, 'folder.jpg')
        else:
            img = ''
        hasher.update(local_path)
        file_key = hasher.hexdigest()
        tags = _get_tags(filepath)
        media = Media()
        media.type = content_type
        media.path = filepath
        media.filename = filename
        media.file_id = file_key
        media.tags = tags
        media.img = img
        media.type = content_type
        media.save()


def index(root_dir):
    """ Index compatible file types
    """
    audio_types = app.config['AUDIO_TYPES']
    video_types = app.config['VIDEO_TYPES']
    index_content(root_dir, audio_types, content_type='audio')
    index_content(root_dir, video_types, content_type='video')


def config_app(filename, project_root=None, app_instance=None):
    """ Setup application parameters. Held in default.py
    """
    if project_root is None:
        project_root = os.path.abspath(os.path.dirname(__file__))
    else:
        project_root = project_root
    config_path = os.path.join(project_root, 'config', filename)
    if not os.path.exists(config_path):
        raise ValueError('You must have a config file present. No file found at: %s' % config_path)
    app_instance.config.from_pyfile(config_path)
    app.config['PROJECT_ROOT'] = project_root
    content_dir = os.path.join(project_root, app.config['CHROMECAST_CONTENT'])
    app.config['CONTENT_DIR'] = content_dir
    return app_instance


@app.route('/')
def home():
    audio = Media.objects.filter(type='audio')
    video = Media.objects.filter(type='video')
    return render_template('index.html', audiofiles=audio, videofiles=video)

@app.route('/reindex')
def reindex():
    index(app.config['PROJECT_ROOT'])
    return ''


@app.route('/video/<path:file_id>')
def video(filekey=None):
    content_record = Media.objects.get(file_id=filekey)
    return render_template('video.html', record=content_record)

@app.route('/videofile/<path:file_id>')
def video_fileserv(filekey):
    filename = Media.objects.get(file_id=filekey).filename
    return send_file_partial(filename)

@app.route('/audiofile/<path:file_id>')
def audio_fileserv(file_id):
    content_record = Media.objects.get(file_id=file_id)
    filename = content_record.path
    return send_file_partial(filename)

@app.route('/audio/<path:file_id>')
def audio(file_id=None):
    content_record = Media.objects.get(file_id=file_id)
    return render_template('audio.html', record=content_record)

@api.register(name='media', url='/media/')
class MediaView(ResourceView):
    resource = MediaResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]


@api.register(name='playlists', url='/playlists/')
class PlaylistView(ResourceView):
    resource = PlaylistResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]


@app.after_request
def after_request(response):
    """
    Adds the range header info, which can only be known after response is assembled
    """
    response.headers.add('Accept-Ranges', 'bytes')
    return response

if __name__ == '__main__':
    if len(sys.argv) > 0:
        if sys.argv[0] == 'debug':
            run()
    run()
