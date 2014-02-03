#!/usr/bin/env python
import os
import sys
import logging
from logging import StreamHandler
from hashlib import sha1


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
    this_app = config_app(filename='default.py', app_instance=app)
    if this_app.config['DEBUG'] or debug:
        this_app.run(debug=True)
    else:
        this_app.run(debug=True)


def index_content(root_dir, file_types):
    """ Index content files
    """
    hasher = sha1()
    content_dir = os.path.join(root_dir, app.config['CONTENT_DIR'])
    files = file_paths(filtered_walk(content_dir, included_files=file_types, ))
    contentfile_list = list()
    logger.debug('root_dir: %s' % root_dir)
    for contentfile in files:
        logger.debug(contentfile)
        rel_path = os.path.relpath(contentfile, root_dir)
        filepath = os.path.join(root_dir, rel_path)
        filename = os.path.split(contentfile)[1]
        local_path = os.path.relpath(filepath, root_dir)
        hasher.update(local_path)
        file_key = hasher.hexdigest()
        content_record = {
            'filepath': filepath,
            'filename': filename,
            'local_path': local_path,
            'file_key': file_key
        }
        filestore[file_key] = content_record
        contentfile_list.append(content_record)
    return contentfile_list


def index(root_dir):
    """ Main entry module for index portion
    """
    content_files = dict()
    audio_types = app.config['AUDIO_TYPES']
    video_types = app.config['VIDEO_TYPES']
    audio_files = index_content(root_dir, audio_types)
    video_files = index_content(root_dir, video_types)
    content_files['audio'] = audio_files
    content_files['video'] = video_files
    logger.debug(content_files)
    return content_files


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


@app.route('/directory', methods=['GET', 'POST'])
def directory():
    pass

@app.route('/')
def home():
    content_files = index(app.config['PROJECT_ROOT'])
    return render_template('index.html', audiofiles=content_files['audio'], videofiles=content_files['video'])


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
