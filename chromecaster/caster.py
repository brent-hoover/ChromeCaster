#!/usr/bin/env python
import os
import logging
from logging import StreamHandler
import sys

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


def index_podcasts(content_dir):
    """ Index audio files
    """
    files = file_paths(filtered_walk(content_dir, included_files=app.config['AUDIO_TYPES'], ))
    filestore.update({'audio_files': files})
    file_list = [x for x in files]
    logger.debug(content_dir)
    return file_list


def index_videos(content_dir):
    """ Index video files
    """
    logger.debug(content_dir)
    files = file_paths(filtered_walk(content_dir, included_files=app.config['VIDEO_TYPES'], ))
    file_list = [x for x in files]
    filestore.update({'video_files': files})
    return file_list


def config_app(filename, project_root=None, app_instance=None):
    """ Setup application parameters. Held in default.py
    """
    if project_root is None:
        project_root = os.path.abspath(os.path.dirname(__file__))
    else:
        project_root = project_root
    logger.debug('PROJECT ROOT: %s' % project_root)
    config_path = os.path.join(project_root, 'config', filename)
    logger.debug(config_path)
    if not os.path.exists(config_path):
        raise ValueError('You must have a config file present. No file found at: %s' % config_path)
    app_instance.config.from_pyfile(config_path)
    app.config['PROJECT_ROOT'] = project_root
    content_dir = os.path.join(project_root, app.config['CHROMECAST_CONTENT'])
    app.config['CONTENT_DIR'] = content_dir
    return app_instance


def index_content(content_dir):
    """ Main entry module for index portion
    """
    print(content_dir)

@app.route('/directory', methods=['GET', 'POST'])
def directory():
    pass

@app.route('/')
def index():
    content_dir = app.config['CONTENT_DIR']
    logger.debug('content dir: %s' % content_dir)
    filenames = index_podcasts(content_dir)
    videos = index_videos(content_dir)
    return render_template('index.html', filenames=filenames, videos=videos)


@app.route('/video/<path:filename>')
def video(filename=None):
    filename = filename.replace('static', 'movies')
    return render_template('video.html', filename=filename)

@app.route('/movies/<path:filename>')
def fileserv(filename):
    filename = filename.replace('movies', 'static')
    filename = os.path.join('static', filename)
    return send_file_partial(filename)


@app.route('/audio/<path:filename>')
def audio(filename=None):
    return render_template('audio.html', filename=filename)

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