#!/usr/bin/env python
import os
import logging

from flask import Flask
from flask import render_template
from walkdir import filtered_walk, file_paths
from chromecaster.send_file import send_file_partial

logger = logging.getLogger(__name__)

app = Flask(__name__)
filestore = dict()


def index_podcasts(content_dir):
    """ Index audio files
    """
    files = file_paths(filtered_walk(content_dir, included_files=app.config['AUDIO_TYPES'], ))
    filestore.update({'audio_files': files})
    return files


def index_videos(content_dir):
    """ Index video files
    """
    files = file_paths(filtered_walk(content_dir, included_files=app.config['VIDEO_TYPES'], ))
    filestore.update({'video_files': files})
    return files


def config_app(filename='default.py'):
    """ Setup application parameters. Held in default.py
    """
    project_root = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(project_root, 'config', filename)
    logger.debug(config_path)
    if not os.path.exists(config_path):
        raise ValueError('You must have a caster.py config file present')
    app.config.from_pyfile(config_path)
    logger.debug(app.config)
    return app


def index_content(content_dir):
    """ Main entry module for index portion
    """
    print(content_dir)

@app.route('/directory', methods=['GET', 'POST'])
def directory():
    pass

@app.route('/')
def index():
    content_dir = app.config('CHROMECASTER_CONTENT')
    filenames = index_podcasts(content_dir)
    videos = index_videos()
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
    if app.config['DEBUG']:
        app.run(debug=True)
    else:
        app.run()
