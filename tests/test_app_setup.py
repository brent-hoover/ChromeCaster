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
        self.config_file = 'config_for_test.py'

    def test_config_find_content(self):
        from chromecaster.caster import config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        self.assertEqual(app.config['CHROMECAST_CONTENT'], 'test_content')

    def test_index_mp3(self):
        from chromecaster.caster import index_podcasts, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        files = [x for x in index_podcasts(self.test_content_dir)]
        self.assertEqual(self.get_filename(files[0]), 'plang.ogg')

    def test_index_mp4(self):
        from chromecaster.caster import index_videos, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)
        files = [x for x in index_videos(self.test_content_dir)]
        self.assertEqual(self.get_filename(files[0]), 'quickcast-compressed.mp4')

    def test_populate_filestore(self):
        from chromecaster.caster import index_podcasts, index_videos, filestore, config_app, app
        config_app(filename=self.config_file, project_root=self.test_root_dir, app_instance=app)

        audio_files = index_podcasts(self.test_content_dir)
        video_files = index_videos(self.test_content_dir)
        self.assertEqual(self.get_filename(audio_files[0]), 'plang.ogg')
        self.assertEqual(self.get_filename(video_files[0]), 'quickcast-compressed.mp4')
