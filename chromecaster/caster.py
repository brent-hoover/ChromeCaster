#!/usr/bin/env python
import os
import sys
import logging
from logging import StreamHandler
from hashlib import sha1
from mutagen.mp3 import EasyMP3 as MP3
from mutagen.easymp4 import EasyMP4


from flask import Flask
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension
from walkdir import filtered_walk, file_paths

from chromecaster.lib.send_file import send_file_partial

logger = logging.getLogger()
shandler = StreamHandler()
logger.addHandler(shandler)
logger.setLevel(logging.DEBUG)


filestore = dict()
app = Flask(__name__)
toolbar = DebugToolbarExtension(app)


def run(debug=True):
    logger.debug('starting...')
    print('starting......')
    this_app = config_app(filename='default.py', app_instance=app)
    index(app.config['PROJECT_ROOT'])
    if this_app.config['DEBUG'] or debug:
        this_app.run(debug=True)
    else:
        this_app.run(debug=True)


def _get_tags(file_path):
    if '.mp3' in file_path:
        tags = dict()
        easymp3 = MP3(file_path)
        logger.debug(easymp3.keys())
        tags['title'] = easymp3.get('title', [''])[0]
        tags['artist'] = easymp3.get('artist', [''])[0]
        return tags
    else:
        return dict()


def index_content(root_dir, file_types):
    """ Scan the media directory, creating an index of file properties for display and serving
    """
    logger.debug('indexing')
    hasher = sha1()
    content_dir = os.path.join(root_dir, app.config['CONTENT_DIR'])
    files = file_paths(filtered_walk(content_dir, included_files=file_types, ))
    contentfile_list = list()
    for contentfile in files:
        rel_path = os.path.relpath(contentfile, root_dir)
        filepath = os.path.join(root_dir, rel_path)
        filename = os.path.split(contentfile)[1]
        local_path = os.path.relpath(filepath, root_dir)
        hasher.update(local_path)
        file_key = hasher.hexdigest()
        tags = _get_tags(filepath)
        content_record = {
            'filepath': filepath,
            'filename': filename,
            'local_path': local_path,
            'file_key': file_key,
            'tags': tags
        }
        filestore[file_key] = content_record
        contentfile_list.append(content_record)
    return contentfile_list


def index(root_dir):
    """ Index compatible file types
    """
    audio_types = app.config['AUDIO_TYPES']
    video_types = app.config['VIDEO_TYPES']
    audio_files = index_content(root_dir, audio_types)
    video_files = index_content(root_dir, video_types)
    filestore['audio'] = audio_files
    filestore['video'] = video_files
    return filestore


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
    return render_template('index.html', audiofiles=filestore['audio'], videofiles=filestore['video'])


@app.route('/video/<path:filekey>')
def video(filekey=None):
    content_record = filestore[filekey]
    return render_template('video.html', record=content_record)

@app.route('/videofile/<path:filekey>')
def video_fileserv(filekey):
    filename = filestore[filekey]['filepath']
    return send_file_partial(filename)

@app.route('/audiofile/<path:filekey>')
def audio_fileserv(filekey):
    filename = filestore[filekey]['filepath']
    return send_file_partial(filename)

@app.route('/audio/<path:filekey>')
def audio(filekey=None):
    content_record = filestore[filekey]
    return render_template('audio.html', record=content_record)

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
            run(debug=True)
    run()
