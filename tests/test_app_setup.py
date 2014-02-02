#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest


class TestAppSetup(unittest.TestCase):

    def get_filename(self, filepath):
        return os.path.split(filepath)[1]

    def setUp(self):
        self.test_root_dir = os.path.abspath(os.path.dirname(__file__))
        self.test_content_dir = os.path.join(self.test_root_dir, 'test_content')

    def test_config_find_content(self):
        from chromecaster.caster import config_app, app
        config_app()
        self.assertEqual(app.config['CHROMECAST_CONTENT'], 'static/podcasts')

    def test_index_mp3(self):
        from chromecaster.caster import index_podcasts
        files = [x for x in index_podcasts(self.test_content_dir)]
        self.assertEqual(self.get_filename(files[0]), 'plang.ogg')

    def test_index_mp4(self):
        from chromecaster.caster import index_videos
        files = [x for x in index_videos(self.test_content_dir)]
        self.assertEqual(self.get_filename(files[0]), 'quickcast-compressed.mp4')

    def test_populate_filestore(self):
        from chromecaster.caster import index_podcasts, index_videos, filestore, config_app
        config_app()
        index_podcasts(self.test_content_dir)
        index_videos(self.test_content_dir)
        audio_files = [x for x in filestore['audio_files']]
        video_files = [x for x in filestore['video_files']]
        self.assertEqual(self.get_filename(audio_files[0]), 'plang.ogg')
        self.assertEqual(self.get_filename(video_files[0]), 'quickcast-compressed.mp4')
